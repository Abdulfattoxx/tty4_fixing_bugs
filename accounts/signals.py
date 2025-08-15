# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserAccount


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_account(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)
    else:
        # mavjud bo‘lsa ham doim saqlab qo‘yamiz
        instance.account.save()
