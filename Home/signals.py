from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


# @receiver(post_save, sender=models.CartItem)
# def update_cart(sender, instance, created, **kwargs):
#     if created:
#     	cart = models.Cart.objects.get(user=instance.user)
#     	cart.total_items += 1
#     	cart.total_amount += instance.price

# @receiver(post_save, sender=models.CartItem)
# def save_cart(sender, instance, **kwargs):
#     instance.cart.save()


@receiver(post_save, sender=models.User)
def send_verification(sender, instance, created, **kwargs):
    if created:
    	models.VerificationToken.objects.create(user=instance)

@receiver(post_save, sender=models.User)
def save_cart(sender, instance, **kwargs):
	# if not instance.is_verified:
	# 	token = models.VerificationToken.objects.get(user=instance)

	# 	link = token.token
	# 	instance.send_verification(link)
	pass
