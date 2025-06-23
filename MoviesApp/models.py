from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    added_on = models.DateTimeField(
        auto_now_add=True
    )