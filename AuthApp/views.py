from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import forms
# from verify_email.email_handler import send_verification_email, resend_verification_email
from django.contrib.auth.models import User
from BlogApp import models as BlogModels
from django.core.paginator import Paginator
from django.contrib.auth import views as authViews
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import os
# from HivePulse import settings
from HivePulse import settings

# Create your views here.

def loginUser(request):
    form = forms.LoginForm(request.POST)
    if request.user.is_authenticated:
        messages.warning(
            request,
            'You are already logged in!',
            extra_tags='error'
        )
        return redirect('/')
    if request.method == 'POST':
        if form.is_valid():
            attempt = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if attempt:
                login(
                    request,
                    attempt
                )
                messages.success(
                    request,
                    'You are now logged in!',
                    extra_tags='success'
                )
                return redirect('/auth/dashboard')
            else:
                messages.warning(
                    request,
                    'Invalid Username or password!',
                    extra_tags='error'
                )
                return redirect('/auth/login')
        else:
            messages.warning(
                request,
                f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return redirect('/auth/login')
    else:
        return render(
            request,
            'AuthApp/login.html',
            {
                'form': form
            }
        )
        
@login_required(login_url='/auth/login')
def logoutUser(request):
    logout(request)
    messages.success(
        request,
        'You are now logged out of the website!',
        extra_tags='success'
    )
    return redirect('/auth/login')


def registerUser(request):
    form = forms.RegisterForm(request.POST)
    if request.user.is_authenticated:
        messages.warning(
            request,
            'You are already registered on this site!',
            extra_tags='error'
        )
        return redirect('/')
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            email_query = None
            try:
                email_query = User.objects.filter(email = form_email).first()
            except Exception as error:
                email_query = None
            if email_query is None:
                # logic for email verification
                # send_verification_email(request, form)
                # return render(
                #     request,
                #     'AuthApp/register-redirect.html',
                #     {
                        
                #     }
                # )
                form.save()
                messages.success(
                    request,
                    'You are now registered on this website!',
                    extra_tags='success'
                )
                attempt = authenticate(
                    request,
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password1']
                )
                login(
                    request,
                    attempt
                )
                return redirect('/auth/dashboard')
            else:
                messages.warning(
                    request,
                    'This email already exists! Try again with a different one!',
                    extra_tags='error'
                )
                return redirect('/auth/register')
        else:
            messages.warning(
                request,
                f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return redirect('/auth/register')
    else:
        return render(
            request,
            'AuthApp/register.html',
            {
                'form': form
            }
        )
        
@login_required(login_url='/auth/login')
def editUser(request):
    form = forms.UserEditForm(request.POST or None, instance = request.user)
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            email_query = None
            try:
                email_query = User.objects.filter(email = form_email).exclude(pk = request.user.id).first()
            except Exception as error:
                email_query = None
            if email_query is not None:
                messages.warning(
                    request,
                    'Your email is associated with another account! Kindly use a different one',
                    extra_tags='error'
                )
                return redirect('/auth/edit-user')
            else:
                form.save()
                messages.success(
                    request,
                    'Your account details have been edited and saved!',
                    extra_tags='success'
                )
                return redirect('/')
        else:
            messages.warning(
                request,
                f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return redirect('/auth/edit-user')
    else:
        return render(
            request,
            'AuthApp/edit-user.html',
            {
                'form': form
            }
        )
        
@login_required(login_url="/auth/login")
def deleteUser(request):
    if request.method == 'POST':
        user_query = User.objects.filter(id = request.user.id).first()
        user_query.delete()
        messages.success(
            request,
            'Your account has been deleted permanently! We will miss you',
            extra_tags='success'
        )
        return redirect('/')
    else:
        return render(
            request,
            'AuthApp/delete-user.html',
            {
                
            }
        )
        
@login_required(login_url='/auth/login')
def editPassword(request):
    form = forms.UserPasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your password was changed and now you can login with your new password!',
                extra_tags='success'
            )
            return redirect('/')
        else:
            messages.warning(
                request,
                f'Your form has errors: {form.errors}',
                extra_tags='error'
            )
            return redirect('/auth/edit-password')
    else:
        return render(
            request,
            'AuthApp/edit-password.html',
            {
                'form': form
            }
        )
        
@login_required(login_url='/auth/login')
def createProfile(request):
    check = None
    try:
        check = request.user.profile
    except Exception as error:
        check = None
    if check is not None:
        messages.warning(
            request,
            message=f'Your profile already exists!',
            extra_tags='danger'
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
                upload_response = settings.imagekit.upload_file(
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
                extra_tags='danger'
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
def editProfile(request):
    check = None
    try:
        check = request.user.profile
    except Exception as error:
        check = None
    if check is None:
        messages.warning(
            request,
            message=f'You have to create a profile in order to edit it!',
            extra_tags='danger'
        )
        return redirect('/auth/create-profile')
    form = forms.ProfileForm(
        request.POST,
        request.FILES,
        instance=request.user.profile
    )
    print(form.fields)
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
                upload_response = settings.imagekit.upload_file(
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
                extra_tags='danger'
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
def dashboard(request):
    post_query = BlogModels.BlogPost.objects.filter(author = request.user).all().order_by('-pk')
    pagination = Paginator(post_query, 2)
    page = request.GET.get('page')
    posts = pagination.get_page(page)
    return render(
        request,
        'AuthApp/dashboard.html',
        {
            'posts': posts
        }
    )
    
class CustomPasswordResetView(authViews.PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = 'AuthApp/password-reset.html'

class CustomPasswordResetConfirmView(authViews.PasswordResetConfirmView):
    form_class = forms.CustomSetPasswordForm
    template_name = 'AuthApp/password-set.html'