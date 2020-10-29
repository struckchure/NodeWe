from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.User)
def send_verification(sender, instance, created, **kwargs):
    if created:
    	models.VerificationToken.objects.create(user=instance)

@receiver(post_save, sender=models.User)
def save_cart(sender, instance, **kwargs):
	pass
