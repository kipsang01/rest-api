import pytest
from django.urls import reverse_lazy
from rest_framework import status


def test_customer_model(test_customer_1):
    name = test_customer_1.__str__()
    assert name == 'John Doe'


def test_orders_model(test_order_1):
    name = test_order_1.__str__()
    assert name == 'Book'


def test_customer_get_list(api_client, test_customer_1, test_customer_2):
    response = api_client.get(reverse_lazy("customer-list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == test_customer_1.id
    assert data[1]["id"] == test_customer_2.id


def test_orders_get_list(api_client, test_order_1, test_order_2):
    response = api_client.get(reverse_lazy("order-list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == test_order_1.id
    assert data[1]["id"] == test_order_2.id


def test_customer_get_detail(api_client, test_customer_1):
    response = api_client.get(
        reverse_lazy("customer-detail", args=(test_customer_1.id,))
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.data
    assert isinstance(data, dict)
    assert data["id"] == test_customer_1.id


@pytest.mark.parametrize(
    "request_data,expected_status_code",
    [
        pytest.param(
            {"name": 'John Doe', "code": "100", "phone_number": "+254720000000"},
            status.HTTP_201_CREATED,
            id="complete-data",
        ),
        pytest.param(

            {"name": 'John Doe', "code": "200"},
            status.HTTP_400_BAD_REQUEST,
            id="missing-phone_number",
        )
    ],
)
def test_post(api_client, request_data, expected_status_code):
    response = api_client.post(reverse_lazy("customer-list"), data=request_data)
    assert response.status_code == expected_status_code
    if status.is_success(response.status_code):
        response_data = response.data
        for key, value in request_data.items():
            assert response_data['data'][key] == value
