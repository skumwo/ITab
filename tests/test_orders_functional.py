from django.test import TestCase
from django.urls import reverse
from users.models import User
from products.models import Product, Order, OrderItem
from cart.models import CartItem
from unittest.mock import patch


class OrderTestCase(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='1234', role='seller')
        self.buyer = User.objects.create_user(username='buyer', password='1234', role='buyer')
        self.product = Product.objects.create(name="Test Product", price=50, stock=10, seller=self.seller)
        self.client.login(username='buyer', password='1234')

    def test_order_page_access(self):
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 200)

    def test_order_created_from_cart(self):
        CartItem.objects.create(buyer=self.buyer, product=self.product, quantity=1)
        session_id = 'mocked'

        with patch("stripe.checkout.Session.retrieve") as mock_session:
            mock_session.return_value.payment_intent = "pi_1234567890"
            response = self.client.get(reverse('payment_success') + f'?session_id={session_id}')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(buyer=self.buyer).exists())

    def test_order_detail_access(self):
        order = Order.objects.create(buyer=self.buyer, total_amount=50)
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_order_detail_blocked(self):
        other_user = User.objects.create_user(username='hacker', password='pass')
        order = Order.objects.create(buyer=self.buyer, total_amount=50)
        self.client.logout()
        self.client.login(username='hacker', password='pass')
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 404)  # доступ запрещён

    def test_order_success_redirect(self):
        order = Order.objects.create(buyer=self.buyer, total_amount=50)
        response = self.client.get(reverse('order_success', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order Successful")  # Или нужный текст на странице
