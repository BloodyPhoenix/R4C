from django.test import TestCase
from django.db.models import signals
from django.core import mail
from orders.models import Order
from customers.models import Customer
from robots.models import Robot
from orders.signal_receivers import send_email


class TestOrdersApi(TestCase):

    @classmethod
    def setUpTestData(cls):
        customer = Customer.objects.create(**{'email': 'customer@customer.ru'})
        Order.objects.create(**{'customer': customer, 'robot_serial': 'R2-D2'})
        Order.objects.create(**{'customer': customer, 'robot_serial': 'R2-C3'})

    def test_signal_is_registered(self):
        registered_functions = [r[1]() for r in signals.post_save.receivers]
        self.assertIn(send_email, registered_functions)

    def test_email_sent(self):
        robot_data = {'serial': 'R2-D2', 'model': "R2", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_not_sent(self):
        robot_data = {'serial': 'R3-D2', 'model': "R3", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        self.assertEqual(len(mail.outbox), 0)






