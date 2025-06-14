# created manually!
from django.urls import path
from . import views

urlpatterns=[
    path('detail/<int:movie_id>', views.movie_details, name='movie-detail')
]