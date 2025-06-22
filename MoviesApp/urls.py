# created manually!
from django.urls import path
from . import views
# /movie/
urlpatterns=[
    path('detail/<int:movie_id>', views.movie_details, name='movie-detail'),
    path('detail/tv/<int:show_id>', views.show_details, name='show-detail'),
    path('search', views.search_movies, name='movie-search'),
    path('search/tv', views.search_shows, name='show-search'),
    path('', views.popular_movies, name='movie-popular'),
    path('tv', views.popular_shows, name='movie-show-popular'),
]