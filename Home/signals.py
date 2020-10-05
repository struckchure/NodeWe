from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.CartItem)
def update_cart(sender, instance, created, **kwargs):
    if created:
    	cart = models.Cart.objects.get(user=instance.user)
    	cart.total_items += 1
    	cart.total_amount += instance.price

@receiver(post_save, sender=models.CartItem)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()
