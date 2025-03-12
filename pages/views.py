from django.shortcuts import render
from products.models import Product

def home_view(request):
    products = Product.objects.all()  # Получаем все товары
    return render(request, 'home.html', {'products': products})

def contact(request):
    return render(request, 'pages/contact.html')

def faq(request):
    return render(request, 'pages/faq.html')

