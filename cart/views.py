from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem
from products.models import Product, Order, OrderItem, Payment, SellerPayment, Refund
from users.models import User
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from products.utils.logger import Logger
from products.utils.payment_factory import payment_handler_factory
from products.utils.observer import Subject, LoggerObserver, SystemNotificationObserver


# Просмотр корзины
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    })


# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Проверяем, есть ли уже этот товар в корзине
    cart_item, created = CartItem.objects.get_or_create(
        buyer=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'{product.name} added to cart.')
    return redirect('view_cart')

# Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, buyer=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

# Очистка корзины
@login_required
def clear_cart(request):
    CartItem.objects.filter(buyer=request.user).delete()
    messages.success(request, 'Cart cleared.')
    return redirect('view_cart')


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    cart_items = CartItem.objects.filter(buyer=request.user)

    if not cart_items.exists():
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    YOUR_DOMAIN = settings.DOMAIN

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=YOUR_DOMAIN + '/cart/payment/success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/cart/payment/cancel/',
    )

    return JsonResponse({'id': checkout_session.id})


endpoint_secret = 'your-webhook-signing-secret'

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Обработать успешный платеж
        # Тут можно автоматически создать заказ, как в `payment_success`
        # Это зависит от вашей логики

    return HttpResponse(status=200)


@login_required
def payment_success(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    if not cart_items.exists():
        messages.error(request, "Cart is empty.")
        return redirect('view_cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Создаём заказ
    order = Order.objects.create(
        buyer=request.user,
        total_amount=total_price,
        status='pending'
    )

    session_id = request.GET.get("session_id")
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    payment_intent_id = checkout_session.payment_intent

    # Создаём платёж
    payment = Payment.objects.create(
        buyer=request.user,
        order=order,
        payment_type='card',
        amount=total_price,
        status='completed',
        stripe_payment_intent_id=payment_intent_id
    )

    # Обработка через фабрику
    handler = payment_handler_factory(payment.payment_type)
    handler.process(payment)

    Logger().log(f"Processed {payment.payment_type} for order #{order.id}")

    # Выплаты продавцам
    seller_payments = {}

    for item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=item.product,
            seller=item.product.seller,
            quantity=item.quantity,
            price=item.product.price,
            status='pending'
        )
        item.product.stock -= item.quantity
        item.product.save()

        seller_id = item.product.seller.id
        seller_payments[seller_id] = seller_payments.get(seller_id, 0) + item.product.price * item.quantity

    for seller_id, amount in seller_payments.items():
        SellerPayment.objects.create(
            order_item=order.items.first(),  # Привязываем к первому товару
            seller_id=seller_id,
            amount=amount,
            status='pending'
        )

    cart_items.delete()

    subject = Subject()
    subject.attach(SystemNotificationObserver())

    subject.notify({
        "user": item.product.seller,
        "message": f"Ваш товар '{item.product.name}' был куплен пользователем {request.user.username}."
    })

    subject.notify({
        "user": request.user,
        "message": f"Вы оформили заказ №{order.id} на сумму ${total_price}."
    })

    Logger().log(f"User {request.user.username} created order #{order.id}")
    messages.success(request, "Оплата прошла успешно. Заказ оформлен.")
    return redirect('order_success', order_id=order.id)


@login_required
def payment_cancel(request):
    messages.error(request, "Payment was canceled.")
    return redirect('view_cart')


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'cart/order_success.html', {'order': order})


@login_required
def request_refund(request, order_item_id):
    item = get_object_or_404(OrderItem, id=order_item_id, order__buyer=request.user)

    payment = item.order.payments.first()

    # Предотвращаем повторный запрос
    if Refund.objects.filter(order_item=item, approved_by_seller__isnull=True).exists():
        messages.warning(request, "Вы уже отправили запрос на возврат.")
        return redirect('order_detail', order_id=item.order.id)

    Refund.objects.create(
        buyer=request.user,
        payment = payment,
        order_item=item,
        reason=request.POST.get('reason', '')
    )

    # Уведомления
    subject = Subject()
    subject.attach(SystemNotificationObserver())

    subject.notify({
        "user": item.product.seller,
        "message": f"Пользователь {request.user.username} запросил возврат на товар '{item.product.name}'."
    })

    Logger().log(f"Refund requested by {request.user.username} for item #{item.id}")
    messages.success(request, "Запрос на возврат отправлен.")
    return redirect('order_detail', order_id=item.order.id)


@login_required
def seller_refund_list(request):
    refunds = Refund.objects.filter(order_item__seller=request.user, approved_by_seller__isnull=True)
    return render(request, 'cart/refunds/seller_refunds.html', {'refunds': refunds})


@login_required
def approve_refund(request, refund_id):
    refund = get_object_or_404(Refund, id=refund_id, order_item__seller=request.user)
    try:
        stripe.Refund.create(
            payment_intent=refund.payment.stripe_payment_intent_id,
            amount=int(refund.order_item.price * refund.order_item.quantity * 100)
        )
        refund.approved_by_seller = True
        refund.refunded_at = now()
        refund.save()

        refund.order_item.status = 'canceled'
        refund.order_item.save()

        # Уведомление покупателя
        subject = Subject()
        subject.attach(SystemNotificationObserver())

        subject.notify({
            "user": refund.buyer,
            "message": f"Продавец одобрил возврат товара «{refund.order_item.product.name}». Средства возвращены."
        })


        messages.success(request, "Возврат одобрен.")
    except stripe.error.StripeError as e:
        messages.error(request, f"Ошибка Stripe: {e}")
    return redirect('seller_refund_list')


@login_required
def reject_refund(request, refund_id):
    refund = get_object_or_404(Refund, id=refund_id, order_item__seller=request.user)
    refund.approved_by_seller = False
    refund.save()

    subject = Subject()
    subject.attach(SystemNotificationObserver())

    subject.notify({
        "user": refund.buyer,
        "message": f"Продавец отклонил возврат товара «{refund.order_item.product.name}»."
    })

    messages.info(request, "Запрос на возврат отклонён.")
    return redirect('seller_refund_list')


@login_required
def my_refunds(request):
    refunds = Refund.objects.filter(buyer=request.user).select_related('order_item', 'order_item__product')
    return render(request, 'cart/refunds/my_refunds.html', {'refunds': refunds})


@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'cart/my_orders.html', {'orders': orders})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})


@login_required
def seller_orders(request):
    if not request.user.is_seller():
        return redirect('home')

    items = OrderItem.objects.filter(product__seller=request.user).select_related('order', 'product')

    refunds = Refund.objects.filter(order_item__product__seller=request.user).select_related('order_item', 'buyer')

    return render(request, 'cart/seller_orders.html', {
            'items': items,
            'refunds': refunds,
        })



from django.core.mail import send_mail

@login_required
@require_POST
def approve_refund(request, refund_id):
    refund = get_object_or_404(Refund, id=refund_id, order_item__seller=request.user)
    action = request.POST.get("action")

    if action == "approve":
        refund.approved_by_seller = True
        refund.order_item.status = "refund_approved"
        refund.order_item.save()

        # Стягиваем платёж
        payment = refund.payment
        if payment and payment.stripe_payment_intent_id:
            try:
                stripe.Refund.create(payment_intent=payment.stripe_payment_intent_id)
                refund.order_item.status = "canceled"
                refund.order_item.save()
            except Exception as e:
                messages.error(request, f"Ошибка возврата: {e}")
                return redirect("seller_orders")

        order = refund.order_item.order
        if all(item.status == "canceled" for item in order.items.all()):
            order.status = "refunded"
            order.save()

        # Уведомление покупателя
        send_mail(
            subject="Ваш возврат одобрен",
            message=f"Ваш запрос на возврат товара «{refund.order_item.product.name}» был одобрен. Средства будут возвращены.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[refund.buyer.email],
            fail_silently=True,
        )

    elif action == "reject":
        refund.approved_by_seller = False

    refund.save()
    messages.success(request, "Решение по возврату сохранено.")
    return redirect('seller_orders')

@login_required
def my_notifications(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})
