from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    slug = models.SlugField(default=slugify(name))
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )
    def make_slug(self):
        self.slug = slugify(self.name)
    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.make_slug()
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.slug} - {self.added_by.username}'

class BlogPosts(models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    tagline = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    content = RichTextField()
    # thumbnail = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to='images/BlogThumnails'
    # )
    thumbnail = models.URLField(
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post_date = models.DateField(
        auto_now_add=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False,
        unique=False
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='post_likes'
    )
    comments = GenericRelation(Comment)
    slug = models.SlugField()
    hide_post = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title} - {self.slug} - {self.author.username}'
    
    def total_likes(self):
        return self.likes.count()
    
    def make_slug(self):
        self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        if not self.slug or self.title != self.__class__.objects.get(pk=self.pk).title:
            self.make_slug()
        super().save(*args, **kwargs)
    
class Service(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f'{self.name} | {self.added_by} | {self.added_at}'
    
    
class Contact(models.Model):
    name = models.CharField(
        max_length = 255,
        null=False,
        blank=False
    )
    subject = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    email = models.EmailField(
        blank=False,
        null=False
    )
    message = models.TextField(
        null=False,
        blank=False
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.subject} | {self.submitted_at}'

class Newsletter(models.Model):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'
    
class Quotation(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    email = models.EmailField(
        null=False,
        blank=False
    )
    service = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    message = models.TextField(
        null=False,
        blank=False
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} | {self.service} | {self.submitted_at}'