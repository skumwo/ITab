import pytest
from products.models import Product
from products.utils.sort_strategies import sort_by_price

@pytest.mark.django_db
def test_sort_by_price():
    Product.objects.create(name="Item A", price=5)
    Product.objects.create(name="Item B", price=15)

    qs = Product.objects.all()
    sorted_qs = sort_by_price(qs)

    prices = list(sorted_qs.values_list("price", flat=True))
    assert prices == [5, 15]
