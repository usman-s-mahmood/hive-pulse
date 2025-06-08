from django.contrib import admin
from . import models

from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.BlogPost)
admin.site.register(models.Contact)
admin.site.register(models.Newsletter)
