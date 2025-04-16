import pytest
from django.urls import reverse
from products.models import Product, Order, OrderItem
from cart.models import CartItem
from users.models import User

@pytest.mark.django_db

def test_order_creation_after_payment(client, mocker):
    seller = User.objects.create_user(username="seller", password="1234", role="seller")
    user = User.objects.create_user(username="buyer", password="1234", role="buyer")
    product = Product.objects.create(name="Phone", price=200, stock=10, seller=seller)
    CartItem.objects.create(buyer=user, product=product, quantity=1)

    client.login(username="buyer", password="1234")

    mock_checkout = mocker.patch("stripe.checkout.Session.retrieve")
    mock_checkout.return_value.payment_intent = "pi_1234567890"

    response = client.get(reverse("payment_success") + "?session_id=mocked")

    assert response.status_code == 302
    assert Order.objects.filter(buyer=user).exists()
