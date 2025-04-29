from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
from products.models import Product, OrderItem, Order
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def chat_list(request):
    user = request.user
    chats = Chat.objects.filter(buyer=user) | Chat.objects.filter(seller=user)
    chats = chats.distinct().order_by('-updated_at')
    return render(request, 'chat/chat_list.html', {'chats': chats})


@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    messages = chat.messages.all().order_by('created_at')

    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=message_text
            )
            return redirect('chat_view', chat_id=chat.id)

    return render(request, 'chat/chat.html', {
        'chat': chat,
        'chat_messages': chat.messages.all().order_by('created_at')
    })


@login_required
def create_chat(request, id, mode):
    if mode == 'product':
        # Покупатель инициирует по product.id
        product = get_object_or_404(Product, id=id)
        seller = product.seller
        buyer = request.user
    elif mode == 'orderitem':
        # Продавец инициирует по order_item.id
        order_item = get_object_or_404(OrderItem, id=id)
        product = order_item.product
        seller = order_item.seller
        buyer = order_item.order.buyer
    else:
        # Неверный режим
        return redirect('home')  # Или другая ошибка обработка

    # Ищем или создаем чат
    chat = Chat.objects.filter(seller=seller, buyer=buyer, product=product).first()
    if not chat:
        chat = Chat.objects.create(seller=seller, buyer=buyer, product=product)

    return redirect('chat_view', chat_id=chat.id)

