from django.db.models import signals
from django.core.mail import send_mail
from django.db import Error
from .models import Order
from robots.models import Robot
from smtplib import SMTPException

PROMOTION_MESSAGE = '''
    Добрый день!
    Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    '''


def send_email(sender, instance, created, **kwargs):
    serial = instance.serial
    orders = Order.objects.select_related('customer').only('customer__email').filter(robot_serial=serial)
    model = instance.model
    version = instance.version
    text = PROMOTION_MESSAGE.format(model=model, version=version)
    for order in orders:
        try:
            send_mail(
                subject=f"Робот {serial} теперь в наличии!",
                message=text,
                from_email='robot_company@robots.com',
                recipient_list=[order.customer.email])
            try:
                # If we need to keep orders history, change this code and do something else to avoid duplicate emails
                order.delete()
            except Error as exception:
                # Logging or sending message if email was sent, but there was no operation with order entity
                pass
        except SMTPException as exception:
            # Logging or sending email seding error
            pass


signals.post_save.connect(send_email, Robot)
