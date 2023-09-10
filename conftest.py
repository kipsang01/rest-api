import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from api.models import Order, Customer

User = get_user_model()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="Tester", email="test@example.com", password='ducfsgykhcjiD4w')
    return user


@pytest.fixture
def api_client(db, test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.fixture
def test_customer_1(db):
    message, _ = Customer.objects.get_or_create(
        name="John Doe",
        code="100",
        phone_number="+254722222222",
    )
    return message


@pytest.fixture
def test_customer_2(db):
    customer, _ = Customer.objects.get_or_create(
        name="John Doe",
        code="200",
        phone_number="+254720000000",
    )
    return customer


@pytest.fixture
def test_order_1(db, test_customer_1):
    order, _ = Order.objects.get_or_create(
        customer=test_customer_1,
        item="Book",
        amount=100.00,
    )
    return order


@pytest.fixture
def test_order_2(db, test_customer_2):
    order, _ = Order.objects.get_or_create(
        customer=test_customer_2,
        item="Book2",
        amount=100.00,
    )
    return order
