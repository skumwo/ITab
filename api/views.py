from rest_framework import viewsets
from cart.models import CartItem
from users.models import User
from products.models import Category, Product, Favorite, Order, OrderItem, Payment, SellerPayment
from .serializers import (
    CategorySerializer, ProductSerializer, FavoriteSerializer, CartItemSerializer, UserSerializer,
    OrderSerializer, OrderItemSerializer, PaymentSerializer, SellerPaymentSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class SellerPaymentViewSet(viewsets.ModelViewSet):
    queryset = SellerPayment.objects.all()
    serializer_class = SellerPaymentSerializer
