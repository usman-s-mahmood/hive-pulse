from django.shortcuts import render, redirect
from django.contrib import messages
from BlogApp import models as blog_models
from BlogApp import views as blog_views
from helpers import TMDB_API
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.

def movie_details(request, movie_id):
    result = TMDB_API.get_movie_details(movie_id=movie_id)
    cast = TMDB_API.get_movie_cast(movie_id=movie_id)
    liked_status = False
    if request.user.is_authenticated:
        query = models.LikedMovies.objects.filter(
            movie_id=movie_id,
            liked_by=request.user.id
        )
        if query.exists():
            liked_status = True
    return render(
        request,
        'MoviesApp/movie-details.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'movie': result,
            'movie_id': movie_id,
            'cast': cast['cast'],
            'liked_status': liked_status,
        }
    )
    
def show_details(request, show_id):
    result = TMDB_API.get_tv_show_details(tv_id=show_id)
    cast = TMDB_API.get_tv_cast(tv_id=show_id)
    liked_status = False
    if request.user.is_authenticated:
        query = models.LikedShows.objects.filter(
            show_id=show_id,
            liked_by=request.user.id
        )
        if query.exists():
            liked_status = True
    return render(
        request,
        'MoviesApp/show-details.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'show': result,
            'show_id': show_id,
            'cast': cast['cast'],
            'liked_status': liked_status,
        }
    )
    
def search_movies(request):
    search = request.GET.get('search')
    page = int(request.GET.get('page'))
    is_tv = bool(request.GET.get('TV'))
    if (is_tv):
        return redirect(f'/movie/search/tv?page={page}&search={search}')
    results = TMDB_API.search_movies_by_title(
        title=search,
        page=page
    )
    print(results)
    return render(
        request,
        'MoviesApp/search-movies.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'results': results,
            'query': search,
            'total_results': results['total_results'],
            'total_pages': results['total_pages'],
            'current_page': page
        }
    )
    
    

def search_shows(request):
    search = request.GET.get('search')
    page = int(request.GET.get('page'))
    results = TMDB_API.search_tv_shows_by_title(
        title=search,
        page=page
    )
    return render(
        request,
        'MoviesApp/search-shows.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'results': results,
            'query': search,
            'total_results': results['total_results'],
            'total_pages': results['total_pages'],
            'current_page': page
        }
    )

def popular_movies(request):
    page = request.GET.get('page')
    results = TMDB_API.get_popular_movies(
        page=page
    )
    
    return render(
        request,
        'MoviesApp/popular-movies.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'results': results,
            'total_results': results['total_results'],
            'total_pages': results['total_pages'],
            'current_page': page,
            'movie': True
        }
    )

def popular_shows(request):
    page = request.GET.get('page')
    results = TMDB_API.get_popular_shows(
        page=page
    )
    
    return render(
        request,
        'MoviesApp/popular-shows.html',
        {
            'recents': blog_models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': blog_views.return_categories(),
            'results': results,
            'total_results': results['total_results'],
            'total_pages': results['total_pages'],
            'current_page': page,
            'show': True
        }
    )    

@login_required(login_url='/auth/login')
def like_movies(request):
    movie_id=int(request.GET.get('movie_id'))
    result = TMDB_API.get_movie_details(
        movie_id=movie_id
    )
    if movie_id is None:
        messages.warning(
            request,
            message=f'Invalid Operation! movie ID not provided',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    if result == None:
        messages.warning(
            request,
            message=f'Invalid Operation! Requested Resource Not Found',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    movie_query = models.LikedMovies.objects.filter(
        liked_by=request.user.id,
        movie_id=movie_id
    )
    
    if movie_query.exists():
        messages.warning(
            request,
            message=f'This Movie is already liked by you!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    movie = models.LikedMovies.objects.create(
        movie_id=movie_id,
        liked_by=request.user,
        title=result['original_title'],
        poster_path=result['poster_path'],
        movie_rating=result['vote_average']
    )
    messages.success(
        request,
        message=f'{result['original_title']} is added to your wishlist',
        extra_tags='success'
    )
    return redirect('/auth/dashboard')


@login_required(login_url='/auth/login')
def like_shows(request):
    show_id=int(request.GET.get('show_id'))
    result = TMDB_API.get_tv_show_details(
        tv_id = show_id
    )
    if show_id is None:
        messages.warning(
            request,
            message=f'Invalid Operation! TV Show ID not provided',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    if result == None:
        messages.warning(
            request,
            message=f'Invalid Operation! Requested Resource Not Found',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    show_query = models.LikedShows.objects.filter(
        liked_by=request.user.id,
        show_id=show_id
    )
    
    if show_query.exists():
        messages.warning(
            request,
            message=f'This Movie is already liked by you!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    show = models.LikedShows.objects.create(
        show_id=show_id,
        liked_by=request.user,
        title=result['original_name'],
        poster_path=result['poster_path'],
        show_rating=result['vote_average']
    )
    messages.success(
        request,
        message=f'{result['original_name']} is added to your wishlist',
        extra_tags='success'
    )
    return redirect('/auth/dashboard')

@login_required(login_url='/auth/login')
def unlike_shows(request):
    show_id=int(request.GET.get('show_id'))

    show_query = models.LikedShows.objects.filter(
        liked_by=request.user.id,
        show_id=show_id
    )
    
    if not show_query.exists():
        messages.warning(
            request,
            message=f'Invalid Operation! This movie is not liked by you!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    title = show_query.first().title
    show_query.delete()
    messages.success(
        request,
        message=f'{title} is removed from your wishlist',
        extra_tags='success'
    )
    return redirect('/auth/dashboard')

@login_required(login_url='/auth/login')
def unlike_movies(request):
    movie_id=int(request.GET.get('movie_id'))
    movie_query = models.LikedMovies.objects.filter(
        liked_by=request.user.id,
        movie_id=movie_id
    )
    
    if not movie_query.exists():
        messages.warning(
            request,
            message=f'Invalid Operation! This Movie is not liked by you!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard')
    title = movie_query.first().title
    movie_query.delete()
    messages.success(
        request,
        message=f'{title} is removed from your wishlist',
        extra_tags='success'
    )
    return redirect('/auth/dashboard')




