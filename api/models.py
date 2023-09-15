import os
from dotenv import load_dotenv

from django.contrib.auth.models import AbstractUser
from django.db import models
import africastalking

load_dotenv()


class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    message_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.item

    def notify_customer(self):

        order_summary = f"Item: {self.item} - Amount:{self.amount}"
        message = (f"Hello {self.customer.name}, Your Order {order_summary}"
                   f" has been received please be patient while it's being processed")
        sender = os.getenv("AFRICASTALKING_SENDER_ID")
        recipients = [self.customer.phone_number]
        response = self.send_message(message, sender, recipients)
        if response['Recipients'][0]['statusCode'] == 101:
            self.message_sent = True
            return 'success'
        else:
            return None

    @staticmethod
    def send_message(message, sender, recipients):
        api_key = os.getenv('AFRICASTALKING_API_KEY')
        username = os.getenv('AFRICASTALKING_USERNAME')

        africastalking.initialize(username, api_key)
        sms = africastalking.SMS

        try:
            response = sms.send(message, recipients, sender)
            # {'SMSMessageData': {'Message': 'Sent to 1/1 Total Cost: KES 0.8000 Message parts: 1', 'Recipients': [
            # {'cost': 'KES 0.8000', 'messageId': 'ATXid_4b9777d774f41c40bb5fef825e19944c', 'number': '+254725171930',
            #  'status': 'Success', 'statusCode': 101}]}}
            return response['SMSMessageData']
        except Exception as e:
            return None
