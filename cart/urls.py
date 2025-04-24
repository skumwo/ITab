from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),

    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),

    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),


    path('refund/request/<int:order_item_id>/', views.request_refund, name='request_refund'),
    path('refund/approve/<int:refund_id>/', views.approve_refund, name='approve_refund'),
    path('refund/reject/<int:refund_id>/', views.reject_refund, name='reject_refund'),
    path('seller/refunds/', views.seller_refund_list, name='seller_refund_list'),
    path('refunds/<int:refund_id>/decision/', views.approve_refund, name='approve_refund'),
    path('refunds/my/', views.my_refunds, name='my_refunds'),

]

