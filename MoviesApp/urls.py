# created manually!
from django.urls import path
from . import views

urlpatterns=[
    path('detail/<int:movie_id>', views.movie_details, name='movie-detail'),
    path('detail/tv/<int:show_id>', views.show_details, name='show-detail'),
    path('search', views.search_movies, name='movie-search'),
]