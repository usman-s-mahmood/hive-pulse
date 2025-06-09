from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # profile_pic = models.ImageField(upload_to='images/profile', null=True, blank=True)
    about_user = models.TextField()
    social_link = models.URLField(blank=True, null=True)
    
    profile_pic = models.URLField(
        null=True,
        blank=True
    )
    
    def get_absolute_url(self):
        return (self.profile_pic)

    def __str__(self):
        return str(self.user.username)