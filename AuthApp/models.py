from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    about_user = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    social_link = models.URLField(
        null=True,
        blank=True
    )
    # profile_pic = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to='images/ProfilePictures'
    # )
    
    profile_pic = models.URLField(
        null=True,
        blank=True
    )
    
    def get_absolute_url(self):
        return (self.profile_pic)
    
    def __str__(self):
        return (self.user.username)