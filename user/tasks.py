from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def sendingEmailTask(subject, message, email):
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

