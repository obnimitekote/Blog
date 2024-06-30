from urllib.parse import urlencode

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import UserToken


@receiver(post_save, sender=User)
def send_email_activation_message(
    signal,
    sender,
    instance,
    created,
    **kwargs
):
    if not created: return
    token = UserToken.objects.create(user=instance)
    message = f'''
    Welcome, {instance.first_name} {instance.last_name}!
    Here is the link to confirm your account:
    http://127.0.0.1:8000/email-verification?token={token.token}
    '''
    send_mail(
        'Email activation',
        message,
        'admin@gmail.com',
        [instance.email]
    )
