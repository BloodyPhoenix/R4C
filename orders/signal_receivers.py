from django.db.models import signals
from django.core.mail import send_mail
from django.db import Error
from .models import Order
from robots.models import Robot
from smtplib import SMTPException


def send_email(sender, instance, created, **kwargs):
    serial = instance.serial
    orders = Order.objects.select_related('customer').only('customer__email').filter(robot_serial=serial)
    model = instance.model
    version = instance.version
    text = f'''
    Добрый день!
    Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    '''
    for order in orders:
        try:
            send_mail(
                subject=f"Робот {serial} теперь в наличии!",
                message=text,
                from_email='robot_company@robots.com',
                recipient_list=[order.customer.email])
            try:
                order.delete()
            except Error as exception:
                # Высылаем сообщение, если по какой-то причине емейл ушёл, а заказ так и висит в базе
                pass
        except SMTPException as exception:
            # Тут мы логируем ошибку отправки, если она возникла
            pass


signals.post_save.connect(send_email, Robot)
