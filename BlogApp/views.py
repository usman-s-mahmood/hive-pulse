from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from AuthApp import forms as auth_forms
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
# from django.conf import settings
import os
from HivePulse.settings import imagekit
from HivePulse import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    services = models.Service.objects.all().order_by('-pk')
    return render(
        request,
        'BlogApp/index.html',
        {
            'services': services,
            'home': True
        }
    )
    
@login_required(login_url='/auth/login')
def add_category(request):
    form = forms.AddCategoryForm(request.POST)
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message=f'Invalid Operation! You are not allowed to visit this page',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    if request.method == 'POST':
        if form.is_valid():
            form.instance.added_by = request.user
            category_name = form.cleaned_data['name']
            category_name = category_name.lower()
            form.instance.name = category_name
            # print(form.instance.name)
            form.save()
            messages.success(
                request,
                message=f'Your category is now added to the system!',
                extra_tags='success'
            )
            return redirect('/add-category')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-category.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'BlogApp/add-category.html',
        {
            'form': form,
            'add_category': True
        }
    )
    
@login_required(login_url='/auth/login')
def add_post(request):
    if (request.user.is_active) and (not request.user.is_superuser or not request.user.is_staff):
        messages.warning(
            request,
            message=f'You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    form = forms.AddPostForm(
        request.POST,
        request.FILES
    )
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user
            form.instance.category = models.Category.objects.filter(name=request.POST.get('category')).first()
            post = form.save(commit=False)
            if 'thumbnail_url' in request.FILES:
                image = request.FILES['thumbnail_url']
                # print(image)
                temp_image_path = os.path.join(settings.MEDIA_ROOT, f'tempfiles/blog-thumbnail/{image.name}')
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
                        folder='/hivepulse/blog_thumbnails/'
                    )
                )
                post.thumbnail = upload_response.url
                # print('reached if block')
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
            post.save() # it works!
            # print('post saved!')
            messages.success(
                request,
                message=f'Your post has been added to the system!',
                extra_tags='success'
            )
            print(form.instance.slug)
            return redirect(f'/posts/{form.instance.slug}') 
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-post.html',
                {
                    'form': form,
                    'categories': models.Category.objects.all()
                }        
            )
    return render(
        request,
        'BlogApp/add-post.html',
        {
            'form': form,
            'categories': models.Category.objects.all(),
            'add_post': True
        }
    )
    
@login_required(login_url='/auth/login')
def edit_post(request, id):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message='You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')

    post_query = models.BlogPosts.objects.filter(id=id).first()

    if post_query is None:
        messages.warning(
            request,
            message='Invalid Post ID! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')

    elif post_query.author.id != request.user.id or not request.user.is_superuser:
        messages.warning(
            request,
            message='Invalid Operation! You cannot edit the post of another user',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')

    form = forms.AddPostForm(
        request.POST or None,
        request.FILES or None,
        instance=post_query
    )
    # Preserve original thumbnail
    print(post_query)
    print(post_query.clean_fields)
    original_thumbnail = post_query.thumbnail
    print(f'preserved thumbnail is: {original_thumbnail}')

    if request.method == 'POST':
        if form.is_valid():
            form.instance.category = models.Category.objects.filter(
                name=request.POST.get('category')
            ).first()

            

            post = form.save(commit=False)

            if 'thumbnail_url' in request.FILES:
                image = request.FILES['thumbnail_url']
                temp_image_path = os.path.join(
                    settings.MEDIA_ROOT,
                    f'tempfiles/blog-thumbnail/{image.name}'
                )
                os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
                with open(temp_image_path, 'wb+') as temp_file:
                    for chunk in image.chunks():
                        temp_file.write(chunk)

                upload_response = imagekit.upload_file(
                    file=open(temp_image_path, 'rb'),
                    file_name=image.name,
                    options=UploadFileRequestOptions(
                        folder='/hivepulse/blog_thumbnails/'
                    )
                )
                post.thumbnail = upload_response.url

                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
            else:
                # Restore existing thumbnail if no new one uploaded
                post.thumbnail = original_thumbnail
                print(f'Thumbnail of post is: {post.thumbnail}')
            post.save()

            messages.success(
                request,
                message='Your post has now been edited!',
                extra_tags='success'
            )

            title_slug = post.slug  # Already available from the updated object
            return redirect(f'/posts/{title_slug}')

        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/edit-post.html',
                {
                    'form': form
                }
            )

    else:
        form = forms.AddPostForm(instance=post_query)
        return render(
            request,
            'BlogApp/edit-post.html',
            {
                'form': form,
                'categories': models.Category.objects.all(),
                'edit_post': True
            }
        )
       
@login_required(login_url='/auth/login')
def delete_post(request, id):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed to visit this area!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    post_query = models.BlogPosts.objects.filter(id=id).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Post ID! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    elif post_query.author.id != request.user.id or not request.user.is_superuser:
        messages.warning(
            request,
            message=f'Invalid Operation! You can not the post of another user',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    form = auth_forms.DeleteConfirmation(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = request.user.username
            password = form.cleaned_data['password']
            attempt = authenticate(
                request,
                username=username,
                password=password
            )
            if attempt:
                post_query.delete()
                messages.success(
                    request,
                    message=f'Your post has been deleted!',
                    extra_tags='success'
                )
                return redirect('/auth/dashboard')
            else:
                messages.warning(
                    request,
                    message=f'Invalid Password! Try again',
                    extra_tags='danger'
                )
                return redirect(f'/delete-post/{id}')
        else:
            messages.warning(
                request,
                message=f'You form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect(f'/delete-post/{id}')
    return render(
        request,
        'BlogApp/delete-post.html',
        {
            'form': form,
            'title': post_query.title,
            'author': post_query.author,
            'delete_post': True
        }
    )
    
def return_categories():
    category_query = models.Category.objects.all()
    return [category.name for category in category_query]
    
def blog_posts(request):
    posts = models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')
    pagination = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = pagination.get_page(page)
    return render(
        request,
        'BlogApp/blog-posts.html',
        {
            'posts': posts,
            'recents': models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': return_categories,
            'blog': True
        }
    )
    
def post_view(request, slug):
    # slug = slug.replace('-', ' ')
    # # post_query = models.BlogPosts.objects.filter(title = slug).first()
    # post_id = request.POST.get('post_id')
    # # print('The value of post id through POST method is: ', post_id)
    # post_query = models.BlogPosts.objects.filter(id=post_id).first();
    post_query = models.BlogPosts.objects.filter(
        slug=slug,
        hide_post=False
    ).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Slug! No post exists with this slug',
            extra_tags='danger'
        )
        return redirect('/posts')
    # print(f'{post_query.author.first_name} - {post_query.author.last_name}')
    # print(f'{post_query.author}')
    return render(
        request,
        'BlogApp/post-view.html',
        {
            'post': post_query,
            'recents': models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': return_categories
        }
    )
    
def category_view(request, category):
    category_query = models.Category.objects.filter(slug=category).first()
    if category_query is None:
        messages.warning(
            request,
            message=f'Invalid Category provided!',
            extra_tags='danger'
        )
        return redirect('/posts')
    post_query = models.BlogPosts.objects.filter(
        category=category_query,
        hide_post=False
    ).all()
    postsNone = False
    if not post_query:
        postsNone = True
    pagination = Paginator(post_query, 2)
    page = request.GET.get('page')
    post_query = pagination.get_page(page)
    return render(
        request,
        'BlogApp/category-view.html',
        {
            'posts': post_query,
            'recents': models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': return_categories,
            'category': category,
            'postsNone': postsNone
        }
    )
    
def search_results(request, query):
    post_query = models.BlogPosts.objects.filter(
        content__contains = query,
        hide_post=False
    ).all().order_by('-pk')
    post_check = False
    if post_query:
        post_check = True
    pagination = Paginator(post_query, 2)
    page = request.GET.get('page')
    post_query = pagination.get_page(page)
    return render(
        request,
        'BlogApp/search-results.html',
        {
            'posts': post_query,
            'post_check': post_check,
            'recents': models.BlogPosts.objects.filter(hide_post=False).all().order_by('-pk')[0:3],
            'categories': return_categories,
            'query': query
        }
    )

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        return redirect(f'/search-results/{query}')
    messages.warning(
        request,
        message=f'You forgot to search!',
        extra_tags='danger'
    )
    return redirect('/')

def search_redirect(request):
    messages.warning(
        request,
        message=f'You forgot to search!',
        extra_tags='danger'
    )
    return redirect('/')

def about_view(request):
    return render(
        request,
        'BlogApp/about.html',
        {
            'about': True
        }
    )
    
def contact_view(request):
    form = forms.ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save to DB
            form.save()

            # Compose full message
            full_message = f"New contact form submission:\n\n" \
                           f"Name: {name}\n" \
                           f"Email: {email}\n\n" \
                           f"Message:\n{message}"

            # Send email
            try:
                send_mail(
                    subject=f"Contact Form submission at Hive Pulse {subject}",
                    message=full_message,
                    from_email=settings.EMAIL_HOST_USER,  # or use email
                    recipient_list=[settings.EMAIL_HOST_USER],  # set in settings or use your email directly
                    fail_silently=False,
                )
                messages.success(
                    request,
                    message='Your contact query is submitted and emailed!',
                    extra_tags='success'
                )
                # full_message = f"Dear {name}," \
                #            f"We have recevied your query about [{subject}], that was submitted to hive pulse and our representative will contact you soon in this regard\n" \
                #            f"Best Regards,\n\n" \
                #            f"IT Team, Hive Pulse"
                # send_mail(
                #     subject=f'Contact Form Query Received by Hive Pulse',
                #     message=full_message,
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     recipient_list=[email],
                #     fail_silently=False
                # )
            except Exception as e:
                messages.warning(
                    request,
                    message=f'Form submitted but email failed to send: {str(e)}',
                    extra_tags='error'
                )

            return redirect('/contact')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )

    return render(
        request,
        'BlogApp/contact.html',
        {
            'form': form,
            'contact': True
        }
    )
   
def not_found(request, exception):
    return render(
        request,
        'BlogApp/404.html',
        status=404
    )
    
def server_error(request):
    return render(
        request,
        'BlogApp/500.html',
        status=500
    )
    
@login_required(login_url='/auth/login')
def add_service(request):
    form = forms.AddServiceForm(request.POST)
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message=f'Invalid Operation! You are not allowed to visit this page',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    if request.method == 'POST':
        if form.is_valid():
            form.instance.added_by = request.user
            service_name = form.cleaned_data['name']
            service_name = service_name.lower()
            form.instance.name = service_name
            form.save()
            messages.success(
                request,
                message=f'Your service is now added to the system!',
                extra_tags='success'
            )
            return redirect('/add-service')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'BlogApp/add-service.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'BlogApp/add-service.html',
        {
            'form': form,
            'add_service': True
        }
    )
    
def newsletter_view(request):
    form = forms.NewsletterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            email_query = models.Newsletter.objects.filter(email=email).first()
            if email_query:
                messages.warning(
                    request,
                    message=f'You have already subscribed to our newsletter',
                    extra_tags='danger'
                )
                return redirect('/')
            else:
                form.instance.email = email
                form.save()
                messages.success(
                    request,
                    message=f'Thank you for subscribing to our newsletter!',
                    extra_tags='success'
                )
                return redirect('/')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect('/')
    return redirect('/')

def quotation_view(request):
    form = forms.QuotationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            service = request.POST.get('service')
            message = request.POST.get('message')
            form.instance.name = name
            form.instance.email = email
            form.instance.service = service
            form.instance.message = message
            form.save()
            messages.success(
                request,
                message=f'Thank you for submitting your query! We will contact you soon',
                extra_tags='success'
            )
            return redirect('/')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect('/')
    return redirect('/')

@login_required(login_url='/auth/login')
def like_post(request, post_id):
    post = models.BlogPosts.objects.filter(id=post_id).first()
    if post is None:
        messages.warning(
            request,
            message=f'Invalid URL! No post exists with this ID',
            extra_tags='danger'
        )
        return redirect('/posts')
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.success(
            request,
            message=f'Post Unliked!',
            extra_tags='warning'
        )
        slug = post.slug
        return redirect(f'/posts/{slug}')
    else:
        post.likes.add(request.user)
        messages.success(
            request,
            'Thank you for liking this post!',
            extra_tags='success'
        )
        slug = post.slug
        return redirect(f'/posts/{slug}')
        
@login_required(login_url='/auth/login')
def hide_post(request, post_id):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed in this area',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    post_query = models.BlogPosts.objects.filter(id=post_id).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Post ID! No relevant post found!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')

    if post_query.hide_post != True:
        post_query.hide_post = True
        post_query.save()
        print(f'Post Hidden status: {post_query.hide_post}')
        messages.success(
            request,
            message=f'Post set to hidden!',
            extra_tags='success'
        )
        return redirect('/auth/dashboard')
    messages.warning(
        request,
        message=f'Post is already hidden!',
        extra_tags='danger'
    )
    return redirect('/auth/dashboard')


@login_required(login_url='/auth/login')
def unhide_post(request, post_id):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.warning(
            request,
            message=f'You are not allowed in this area',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    post_query = models.BlogPosts.objects.filter(id=post_id).first()
    if post_query is None:
        messages.warning(
            request,
            message=f'Invalid Post ID! No relevant post found!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')

    if post_query.hide_post != False:
        post_query.hide_post = False
        post_query.save()
        print(f'Post Hidden status: {post_query.hide_post}')
        messages.success(
            request,
            message=f'Post set to unhidden!',
            extra_tags='success'
        )
        return redirect('/auth/dashboard')
    messages.warning(
        request,
        message=f'Post is already unhidden!',
        extra_tags='danger'
    )
    return redirect('/auth/dashboard')