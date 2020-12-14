from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from list.models import Profile, List

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=List)
def connect_list_with_users(sender, instance=None, created=False, **kwargs):
    if created:
        profileone = instance.userone.profile
        profileone.list = instance
        profileone.save()
        profiletwo = instance.usertwo.profile
        profiletwo.list = instance
        profiletwo.save()
