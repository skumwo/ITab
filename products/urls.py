from django.urls import path
from .views import product_list, add_product, buy_product, product_detail, confirm_purchase, update_product, delete_product, add_to_favorites, remove_from_favorites, favorites_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('favorites/add/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', favorites_list, name='favorites_list'),

    path('add/', add_product, name='add_product'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('<int:product_id>/confirm/', confirm_purchase, name='confirm_purchase'),
    path('<int:product_id>/buy/', buy_product, name='buy_product'),
    path('product/<int:pk>/edit/', update_product, name='update_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),

]