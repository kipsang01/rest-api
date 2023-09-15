import pytest
import uuid
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import Order, Customer

User = get_user_model()


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="Tester", password='ducfsgykhcjiD4w')
    return user



@pytest.fixture
def api_client(db, test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.fixture
def unauthenticated_client(db):
    client = APIClient()
    return client


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def test_customer_1(db):
    customer, _ = Customer.objects.get_or_create(
        name="John Doe",
        code="100",
        phone_number="+254722222222",
    )
    return customer


@pytest.fixture
def test_customer_2(db):
    customer, _ = Customer.objects.get_or_create(
        name="John Doe",
        code="200",
        phone_number="+254722222222",
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
