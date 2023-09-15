import os

import pytest
from django.urls import reverse_lazy
from rest_framework import status


def test_unauthorized_request(unauthenticated_client):
    response = unauthenticated_client.get(reverse_lazy('customer-list'))
    assert response.status_code == 401


# def test_authorized_request(unauthenticated_client, get_or_create_token):
#     # unauthenticated_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token.key)
#     response = unauthenticated_client.get(reverse_lazy('customer-list'))
#     assert response.status_code == 200


def test_customer_model(test_customer_1):
    name = test_customer_1.__str__()
    assert name == 'John Doe'


def test_orders_model(test_order_1):
    name = test_order_1.__str__()
    assert name == 'Book'


def test_notify_customer(test_order_1):
    assert test_order_1.message_sent is False
    test_order_1.notify_customer()
    assert test_order_1.message_sent is True


def test_send_message_success(test_order_2):
    message = "Hello world"
    recipients = test_order_2.customer.phone_number
    response = test_order_2.send_message(message, [recipients])
    assert response['Recipients'][0]['statusCode'] == 101


def test_send_message_failure(test_order_2):
    message = "Hello world"
    recipients = test_order_2.customer.phone_number
    response = test_order_2.send_message(message, recipients)
    assert response is None


def test_customer_create():
    pass


def test_orders_create():
    pass


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
    assert response.status_code == status.HTTP_200_OK

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
def test_post_customers(api_client, request_data, expected_status_code):
    response = api_client.post(reverse_lazy("customer-list"), data=request_data)
    assert response.status_code == expected_status_code
    if status.is_success(response.status_code):
        response_data = response.data
        for key, value in request_data.items():
            assert response_data['data'][key] == value

# def get_customer(test_customer_1):
#     return test_customer_1.id
# @pytest.mark.parametrize(
#     "request_data, expected_status_code",
#     [
#         pytest.param(
#             {"item": "Book", "amount": 1000},
#             status.HTTP_201_CREATED,
#             id="complete-data",
#         ),
#         # pytest.param(
#         #
#         #     {"customer": test_customer_1, "item": "Book"},
#         #     status.HTTP_400_BAD_REQUEST,
#         #     id="missing-amount",
#         # ),
#         # pytest.param(
#         #
#         #     {"item": "Book"},
#         #     status.HTTP_400_BAD_REQUEST,
#         #     id="missing-customer",
#         # )
#     ],
# )
# def test_post_orders(api_client, request_data, expected_status_code):
#     response = api_client.post(reverse_lazy("order-list"), data=request_data)
#     assert response.status_code == expected_status_code
#     if status.is_success(response.status_code):
#         response_data = response.data
#         for key, value in request_data.items():
#             assert response_data['data'][key] == value
