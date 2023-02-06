from django.db.models import signals
from django.core.mail import send_mail
from django.db import Error
from .models import Order
from robots.models import Robot
from smtplib import SMTPException


def send_email(sender, instance, created, **kwargs):
    pass


signals.post_save.connect(send_email, Robot)
