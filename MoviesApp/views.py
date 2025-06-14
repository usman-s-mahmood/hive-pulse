from django.shortcuts import render, redirect
from django.contrib import messages
from BlogApp import models as blog_models
from BlogApp import views as blog_views
from helpers import TMDB_API

# Create your views here.

def movie_details(request, movie_id):
    result = TMDB_API.get_movie_details(movie_id=movie_id)
    cast = TMDB_API.get_movie_cast(movie_id=movie_id)
    return render(
        request,
        'MoviesApp/movie-details.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'movie': result,
            'movie_id': movie_id,
            'cast': cast['cast']
        }
    )
    
def show_details(request, show_id):
    result = TMDB_API.get_tv_show_details(tv_id=show_id)
    cast = TMDB_API.get_tv_cast(tv_id=show_id)
    return render(
        request,
        'MoviesApp/show-details.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'show': result,
            'show_id': show_id,
            'cast': cast['cast']
        }
    )