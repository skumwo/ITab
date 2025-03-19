from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm

# Декораторы для проверки ролей
def seller_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'seller':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def buyer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'buyer':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Страница с товарами
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# Страница отдельного продукта
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
@seller_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


@login_required
@seller_required
def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if product.seller != request.user:  # Только собственник товара может редактировать
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/add_product.html', {'form': form})

# Удаление товара
@login_required
@seller_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    if product.seller == request.user:  # Только собственник товара может удалить
        product.delete()
    return redirect('product_list')


# Страница подтверждения покупки
@login_required
@buyer_required
def confirm_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        return redirect('buy_product', product_id=product.id)

    return render(request, 'products/confirm_purchase.html', {'product': product})

# Совершение покупки
@login_required
@buyer_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        raise PermissionDenied("This product is out of stock")

    product.stock -= 1
    product.save()

    return render(request, 'products/success.html', {'product': product})
