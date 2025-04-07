from django.contrib import admin
from .models import Product, Order, OrderItem, Payment, SellerPayment, Category, Favorite, Refund

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(SellerPayment)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Refund)

