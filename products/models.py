from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_items", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    received_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Item {self.product.name} in Order {self.order.id}"

class Payment(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payment_type = models.CharField(max_length=50, choices=[('card', 'Card'), ('paypal', 'PayPal'), ('crypto', 'Crypto')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

class SellerPayment(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="seller_payments")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment to {self.seller.username} - {self.status}"

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")

    def __str__(self):
        return f"{self.buyer.username} likes {self.product.name}"