import pytest
from django.urls import reverse
from products.models import Product
from cart.models import CartItem
from users.models import User

@pytest.mark.django_db
def test_add_to_cart(client):
    user = User.objects.create_user(username="testuser", password="1234")
    product = Product.objects.create(name="Test Product", price=100)

    client.login(username="testuser", password="1234")
    response = client.post(reverse("add_to_cart", args=[product.id]), data={"quantity": 2})

    assert response.status_code == 302  # редирект
    cart_item = CartItem.objects.get(buyer=user, product=product)
    assert cart_item.quantity == 2
