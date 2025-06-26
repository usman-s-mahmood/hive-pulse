from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.LikedMovies)
admin.site.register(models.LikedShows)