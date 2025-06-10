# created manually!
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_save, sender=User)
def check_unique_email(sender, instance, **kwargs):
    # Check if the email already exists
    if instance.email:
        if User.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
            raise ValidationError(f"Email {instance.email} is already in use.")

