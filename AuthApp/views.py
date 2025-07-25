from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from BlogApp.models import BlogPosts
from django.core.paginator import Paginator
from django.conf import settings
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import os
from django.contrib.auth import views as auth_views
from HivePulse.settings import imagekit
from HivePulse import settings
from MoviesApp import models as movie_models
from helpers import knn_movies, knn_shows

# Create your views here.

def login_user(request):
    form = forms.LoginForm(request.POST)
    if request.user.is_authenticated:
        messages.warning(
            request,
            message=f'You are already logged in!',
            extra_tags='error'
        )
        return redirect('/')
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            attempt = authenticate(
                request,
                username=username,
                password=password
            )
            if attempt:
                login(
                    request,
                    attempt
                )
                messages.success(
                    request,
                    message=f'You are now logged into the website',
                    extra_tags='success'
                )
                return redirect('/auth/dashboard')
            else:
                messages.warning(
                    request,
                    message=f'Invalid Username or password!',
                    extra_tags='error'
                )
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
    return render(
        request,
        'AuthApp/login.html',
        {
            'form': form,
            'login': True
        }
    )
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request,
            message=f'Logout Successful!',
            extra_tags='success'
        )
        return redirect('/auth/login')
    else:
        messages.warning(
            request,
            message=f'You have to login to visit this page',
            extra_tags='error'
        )
        return redirect('/auth/login')
    
def register_user(request):
    form = forms.RegisterForm(request.POST)
    if request.user.is_authenticated:
        messages.warning(
            request,
            message=f'You are already registered on this site!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard') 
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            user_query = User.objects.filter(email=form_email).first()
            if user_query:
                messages.warning(
                    request,
                    message=f'This email is already registered with another account! Please try again with a different one',
                    extra_tags='error'
                )
                form.fields['email'].help_text = f'Change this email! It is associated with another account'
                return render(
                    request,
                    'AuthApp/register.html',
                    {
                        'form': form
                    }
                )
            else:
                form.save()
                messages.success(
                    request,
                    message=f'You are now registered in on this site!',
                    extra_tags='success'
                )
                return redirect('/auth/login') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'AuthApp/register.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'AuthApp/register.html',
        {
            'form': form,
            'register': True
        }
    )
    
@login_required(login_url='/auth/login')
def edit_user(request):
    form = forms.CustomUserChangeForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            email_query = User.objects.filter(email=form_email).exclude(pk=request.user.pk).first()
            if email_query:
                messages.warning(
                    request,
                    message=f'Invalid Email! This email is associated with another account',
                    extra_tags='error'
                )
                return render(
                    request,
                    'AuthApp/edit-user.html',
                    {
                        'form': form
                    }
                )
            else:
                form.save()
                messages.success(
                    request,
                    message=f'Your account is now updated!',
                    extra_tags='success'
                )
                return redirect('/auth/dashboard')  
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'AuthApp/edit-user.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'AuthApp/edit-user.html',
        {
            'form': form,
            'edit_user': True
        }
    )
    
@login_required(login_url='/auth/login')
def edit_password(request):
    form = forms.CustomEditPasswordForm(request.user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            form.save()
            update_session_auth_hash(
                request,
                user
            )
            messages.success(
                request,
                message=f'Your password is updated!',
                extra_tags='success'
            )
            return redirect('/auth/dashboard') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return redirect('/auth/edit-password')
    return render(
        request,
        'AuthApp/edit-password.html',
        {
            'form': form,
            'edit_password': True
        }
    )
    
@login_required(login_url='/auth/login')
def delete_user(request):
    form = forms.DeleteConfirmation(request.POST)
    if request.method == 'POST':
        if request.user.is_superuser and request.user.is_staff:
            messages.warning(
                request,
                message=f'Accounts with escalated permissions cannot be deleted!',
                extra_tags='error'
            )
            return redirect('/auth/dashboard')
        if form.is_valid():
            password = form.cleaned_data['password']
            attempt = authenticate(
                request,
                username=request.user.username,
                password=password
            )
            if attempt is not None:
                request.user.delete()
                messages.success(
                    request,
                    message=f'Your account has been deleted successfully!',
                    extra_tags='success'
                )
                return redirect('/')
            else:
                messages.warning(
                    request,
                    message=f'Account deletion not possible due to incorrect password!',
                    extra_tags='error'
                )
                return redirect('/auth/delete-user')
    return render(
        request,
        'AuthApp/delete-user.html',
        {
            'form': form,
            'delete_user': True
        }
    )
    
@login_required(login_url='/auth/login')
def create_profile(request):
    check = None
    try:
        check = request.user.profile
    except Exception as error:
        check = None
    if check is not None:
        messages.warning(
            request,
            message=f'Your profile already exists!',
            extra_tags='error'
        )
        return redirect('/auth/dashboard') 
    form = forms.ProfileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            profile = form.save(commit=False)
            if 'profile_pic_url' in request.FILES:
                image = request.FILES['profile_pic_url']
                # print(image)
                temp_image_path = os.path.join(settings.MEDIA_ROOT, f'tempfiles/profile-pictures/{image.name}')
                os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
                with open(temp_image_path, 'wb+') as temp_file:
                    for chunk in image.chunks():
                        temp_file.write(chunk)
                upload_response = imagekit.upload_file(
                    file=open(
                        temp_image_path, 
                        'rb'
                    ),
                    file_name=image.name,
                    options=UploadFileRequestOptions(
                        folder='/hivepulse/profile_pictures/'
                    )
                )
                profile.profile_pic = upload_response.url
                # print('reached if block')
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                models.ImageUpload.objects.create(
                    uploaded_by = request.user,
                    image_url = upload_response.url,
                    image_type = 'ProfilePicture',
                )
            profile.save()
            messages.success(
                request,
                message=f'Your Profile has been created successfully!',
                extra_tags='success'
            )
            return redirect('/auth/dashboard') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'AuthApp/create-profile.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'AuthApp/create-profile.html',
        {
            'form': form,
            'create_profile': True
        }
    )
    
@login_required(login_url='/auth/login')
def edit_profile(request):
    check = None
    try:
        check = request.user.profile
    except Exception as error:
        check = None
    if check is None:
        messages.warning(
            request,
            message=f'You have to create a profile in order to edit it!',
            extra_tags='error'
        )
        return redirect('/auth/create-profile')
    form = forms.ProfileForm(
        request.POST,
        request.FILES,
        instance=request.user.profile
    )
    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_pic_url' in request.FILES:
                image = request.FILES['profile_pic_url']
                # print(image)
                temp_image_path = os.path.join(settings.MEDIA_ROOT, f'tempfiles/profile-pictures/{image.name}')
                os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
                with open(temp_image_path, 'wb+') as temp_file:
                    for chunk in image.chunks():
                        temp_file.write(chunk)
                upload_response = imagekit.upload_file(
                    file=open(
                        temp_image_path, 
                        'rb'
                    ),
                    file_name=image.name,
                    options=UploadFileRequestOptions(
                        folder='/hivepulse/profile_pictures/'
                    )
                )
                profile.profile_pic = upload_response.url
                # print('reached if block')
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                models.ImageUpload.objects.create(
                    uploaded_by = request.user,
                    image_url = upload_response.url,
                    image_type = 'ProfilePicture',
                )
            profile.save()
            messages.success(
                request,
                message=f'Your Profile has been updated!',
                extra_tags='success'
            )
            return redirect('/auth/dashboard') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'AuthApp/edit-profile.html',
                {
                    'form': form
                }
            )
    else:
        form = forms.ProfileForm(
            instance=request.user.profile
        )
        return render(
            request,
            'AuthApp/edit-profile.html',
            {
                'form': form,
                'edit_profile': True
            }
        )
        
@login_required(login_url='/auth/login')
def user_dashboard(request):
    post_query = BlogPosts.objects.filter(author=request.user).all().order_by('-pk')
    post_none = True
    if post_query is not None:
        post_none = False
    pagination = Paginator(post_query, 3)
    page = request.GET.get('post_page')
    post_query = pagination.get_page(page)
    user_posts = BlogPosts.objects.filter(
        likes=request.user, 
        hide_post=False
    ).all().order_by('-pk')
    user_post_none = True
    if user_posts is not None:
        user_post_none = False
    user_pagination = Paginator(user_posts, 4)
    user_page = request.GET.get('like_page')
    user_posts = user_pagination.get_page(user_page)
    
    movies_query = movie_models.LikedMovies.objects.filter(
        liked_by=request.user
    ).all().order_by('-pk')
    movies_none = True
    if movies_query.exists():
        movies_none = False
    movie_pagination = Paginator(movies_query, 4)
    movie_page = request.GET.get('movie_page')
    movies = movie_pagination.get_page(movie_page)
    
    shows_query = movie_models.LikedShows.objects.filter(
        liked_by = request.user,
    ).all().order_by('-pk')
    shows_none = True
    if shows_query.exists():
        shows_none = False
    show_pagination = Paginator(shows_query, 4)
    show_page = request.GET.get('show_page')
    shows = show_pagination.get_page(show_page)

    liked_shows_count = shows_query.count()
    liked_movies_count = movies_query.count()

    k_shows = 4
    if request.GET.get('k_shows'):
        print("I got K shows value!")
        k_shows = int(request.GET.get('k_shows'))
        if k_shows > liked_shows_count:
            k_shows=liked_shows_count
            messages.warning(
                request,
                message=f'Recommendation can not be greater total number of liked shows',
                extra_tags='error'
            )
            
    k_movies = 4
    if request.GET.get('k_movies'):
        print("I got K movies value!")
        k_movies = int(request.GET.get('k_movies'))
        if k_movies > liked_movies_count:
            k_movies=liked_movies_count
            messages.warning(
                request,
                message=f'Recommendation can not be greater total number of liked movies',
                extra_tags='error'
            )
    
    recommended_shows = knn_shows.recommend_shows_knn(
        user=request.user,
        k=k_shows
    )
    recommended_movies = knn_movies.recommend_movies_knn(
        user=request.user,
        k=k_movies
    )
    print(recommended_movies)

    return render(
        request,
        'AuthApp/dashboard.html',
        {
            'post_none': post_none,
            'posts': post_query,
            'dashboard': True,
            'user_post_none': user_post_none,
            'user_posts': user_posts,
            'movies': movies,
            'movies_none': movies_none,
            'shows': shows,
            'shows_none': shows_none,
            'recommended_shows': recommended_shows,
            'recommended_movies': recommended_movies,
            'liked_shows_count': liked_shows_count,
            'liked_movies_count': liked_movies_count,
        }
    )
    
# forgot password implementation

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = 'AuthApp/forgot-password/password-reset.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = forms.CustomSetPasswordForm
    template_name = 'AuthApp/forgot-password/password-set.html'
    
# handling email duplication error
# @login_required(login_url='/auth/login')
# def email_duplication(request, email):
#     if request.user.is_superuser or request.user.is_staff:
#         email_query = User.objects.filter(email=email).first()
#         if email_query:
#             messages.warning(
#                 request,
#                 message=f'You are using an email that is associated with another user!',
#                 extra_tags='error'
#             )
#             return render(
#                 request,
#                 'AuthApp/email-duplication.html',
#                 {
                    
#                 }
#             )
#         else:
#             messages.warning(
#                 request,
#                 message=f'You can not visit this page without any reason!',
#                 extra_tags='error'
#             )
#             return redirect('/auth/dashboard')
#     else:
#         messages.warning(
#             request,
#             message=f'Invalid Operation! You can not visit this page',
#             extra_tags='error'
#         )
#         return redirect('/auth/dashboard')