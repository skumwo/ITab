from rest_framework import serializers
from products.models import Category, Product, Favorite, Order, OrderItem, Payment, SellerPayment
from cart.models import CartItem
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

class SellerPaymentSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SellerPayment
        fields = '__all__'
