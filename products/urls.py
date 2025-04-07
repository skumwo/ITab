from django.urls import path
from .views import product_list, add_product, buy_product, product_detail, confirm_purchase, update_product, delete_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('<int:product_id>/', product_detail, name='product_detail'),  # Просмотр продукта
    path('<int:product_id>/confirm/', confirm_purchase, name='confirm_purchase'),  # Подтверждение покупки
    path('<int:product_id>/buy/', buy_product, name='buy_product'),  # Совершение покупки
    path('product/<int:pk>/edit/', update_product, name='update_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),

]