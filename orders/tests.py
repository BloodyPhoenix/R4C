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

    def test_correct_email_content(self):
        robot_data = {'serial': 'R2-D2', 'model': "R2", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        self.assertEqual(mail.outbox[0].subject, "Робот R2-D2 теперь в наличии!")

    def test_multiple_emails_sent(self):
        customer = Customer.objects.create(**{'email': 'customer_2@customer.ru'})
        Order.objects.create(**{'customer': customer, 'robot_serial': 'R2-D2'})
        robot_data = {'serial': 'R2-D2', 'model': "R2", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        self.assertEqual(len(mail.outbox), 2)

    def test_proper_order_deleted(self):
        order_1 = Order.objects.get(robot_serial='R2-D2')
        order_2 = Order.objects.get(robot_serial='R2-C3')
        robot_data = {'serial': 'R2-D2', 'model': "R2", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        orders = Order.objects.all()
        self.assertNotIn(order_1, orders)
        self.assertIn(order_2, orders)

    def test_multiple_orders_deleted(self):
        customer = Customer.objects.create(**{'email': 'customer_2@customer.ru'})
        Order.objects.create(**{'customer': customer, 'robot_serial': 'R2-D2'})
        orders = Order.objects.filter(robot_serial='R2-D2')
        robot_data = {'serial': 'R2-D2', 'model': "R2", 'version': 'D2', 'created': '2022-12-31 23:59:59'}
        Robot.objects.create(**robot_data)
        all_orders = Order.objects.all()
        for order in orders:
            self.assertNotIn(order, all_orders)






