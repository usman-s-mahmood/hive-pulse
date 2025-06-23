from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LikedShows(models.Model):
    show_id = models.IntegerField(
        unique=False,
        null=False,
        blank=False
    )
    liked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    title = models.TextField(
        null=False,
        blank=False
    )
    poster_path = models.TextField(
        null=False,
        blank=False
    )
    show_rating = models.FloatField(
        null=False,
        blank=False
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f'{self.liked_by.username} | {self.title} | {self.added_on}'



class LikedMovies(models.Model):
    movie_id = models.IntegerField(
        unique=False,
        null=False,
        blank=False
    )
    liked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    title = models.TextField(
        null=False,
        blank=False
    )
    poster_path = models.TextField(
        null=False,
        blank=False
    )
    movie_rating = models.FloatField(
        null=False,
        blank=False
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f'{self.liked_by.username} | {self.title} | {self.added_on}'
    



 