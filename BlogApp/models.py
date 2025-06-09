from django.db import models
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=500, unique=True, null=False, blank=False)
    added_by = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.name} | added by: {self.added_by}'
    
class BlogPost(models.Model):
    title = models.TextField()
    tagline = models.TextField()
    # thumbnail = models.ImageField(upload_to='images/blog-thumbnails', null = True, blank = True)
    thumbnail = models.URLField(
        null=True,
        blank=True
    )
    category = models.CharField(max_length=500)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date_posted = models.DateField(auto_now_add = True)
    likes = models.ManyToManyField(User, blank = True, related_name="post_likes")
    
    def __str__(self):
        return f'{self.title} | posted by: {self.author.username}'
    
    def total_likes(self):
        return self.likes.count()
    
class Contact(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    subject = models.CharField(max_length = 250, default = None)
    message = models.TextField()
    date_contacted = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.name} | {self.date_contacted}'
    
class Newsletter(models.Model):
    email = models.EmailField()
    date_subscribed = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.email}'
    
    
# class Appointments(models.Model):
#     name = models.CharField(max_length = 500)
#     email = models.EmailField()
#     phone_number = PhoneNumberField()
#     service = models.CharField(max_length = 100)
#     appointment_date = models.DateField()
#     appointment_time = models.CharField(max_length=50)
#     message = models.TextField()
#     submission_date = models.DateTimeField(auto_now_add = True)

#     def __str__(self):
#         return f'{self.name} | {self.appointment_date} | {self.service}'
    
# class Services(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    added_by = models.CharField(max_length = 500)
    
    def __str__(self):
        return f'{self.name}'