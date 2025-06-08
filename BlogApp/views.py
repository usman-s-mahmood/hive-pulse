from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.core.mail import send_mail
from datetime import datetime, date
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    # form = forms.AppointmentForm(request.POST or None)

    return render(
        request,
        'BlogApp/index.html',
        {
            
        }
    )
    
@login_required(login_url='/auth/login')
def addCategory(request):
    form = forms.AddCategoryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form_category = form.cleaned_data['name']
            category_query = None
            try:
                category_query = models.Category.objects.filter(name = form_category).first()
            except Exception as error:
                category_query = None
            if category_query is None:
                form.instance.added_by = request.user.username
                form.save()
                messages.success(
                    request,
                    f'Your category: {form_category} is now added to the database',
                    extra_tags='success'
                )
                return redirect('/add-category')
            else:
                messages.warning(
                    request,
                    'This category already exists!',
                    extra_tags='error'
                )
                return redirect('/add-category')
        else:
            messages.warning(
                request,
                f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'BlogApp/add-category.html',
                {
                    'form': form
                }
            )
    else:
        return render(
            request,
            'BlogApp/add-category.html',
            {
                'form': form
            }
        )
        
@login_required(login_url='/auth/login')
def addPost(request):
    form = forms.AddBlogPostForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(
                request,
                'Your post has been added!',
                extra_tags='success'
            )
            return redirect(f'/post-view/{form.cleaned_data['title'].replace(' ', '-')}/{form.instance.pk}')
        else:
            messages.warning(
                request,
                f'Your form has errors!{form.errors}',
                extra_tags='error'
            )
            return render(
                request,
                'BlogApp/add-post.html',
                {
                    'form': form
                }
            )
    else:
        return render(
            request,
            'BlogApp/add-post.html',
            {
                'form': form
            }
        )
        
@login_required(login_url='/auth/login')
def editPost(request, slug, post_id):
    post_query = None
    try:
        post_query = models.BlogPost.objects.filter(pk = post_id, title = slug.replace('-', ' ')).first()
    except Exception as error:
        post_query = None
    if post_query == None:
        messages.warning(
            request,
            'No such post exists in the database!',
            extra_tags='error'
        )
        return redirect('/')
    elif post_query != None and post_query.author == request.user:
        form = forms.AddBlogPostForm(request.POST, request.FILES, instance = post_query)
        if request.method == 'POST':
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                messages.success(
                    request,
                    'Your post has now been edited!',
                    extra_tags='success'
                )
                return redirect(f'/post-view/{form.cleaned_data['title'].replace(' ', '-')}/{form.instance.pk}')
            else:
                messages.warning(
                    request,
                    f'Your form has errors!\n{form.errors}',
                    extra_tags='error'
                )
                form = forms.AddBlogPostForm(instance = post_query)
                return render(
                    request,
                    'BlogApp/edit-post.html',
                    {
                        'form': form
                    }
                )
        else:
            form = forms.AddBlogPostForm(instance = post_query)
            return render(
                request,
                'BlogApp/edit-post.html',
                {
                    'form': form
                }
            )
    else:
        messages.warning(
            request,
            'You can only edit your posts! This post is associated with another user',
            extra_tags='error'
        )
        return redirect('/')
    
@login_required(login_url='/auth/login')
def deletePost(request, post_id):
    post_query = None
    try:
        post_query = models.BlogPost.objects.filter(id = post_id).first()
    except Exception as error:
        post_query = None
    if post_query is None:
        messages.warning(
            request,
            'This post does not exist!',
            extra_tags='error'
        )
        return redirect('/')
    elif post_query != None:
        if post_query.author == request.user:
            if request.method == 'POST':
                post_query.delete()
                messages.success(
                    request,
                    'Your post is now deleted!',
                    extra_tags='success'
                )
                return redirect('/')
            return render(
                request,
                'BlogApp/delete-post.html',
                {
                    'title': post_query.title
                }
            )
        else:
            messages.warning(
                request,
                'You can not delete posts associated with other users!',
                extra_tags='error'
            )
            return redirect('/')
    else:
        messages.warning(
            request,
            'Error in fetching content from database!',
            extra_tags='error'
        )
        return redirect('/')
    
def contactView(request):
    form = forms.ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail(
                    subject = "Contact Query from Upwave Builders Blog!",
                    message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nmessage: {message}",
                    recipient_list=['muhammadusman27virgo@yahoo.com'],
                    from_email='muhammadusman27virgo@yahoo.com'
                )
            except Exception as error:
                with open('logs.txt', 'a') as file:
                    file.write(f'\n===============================================\nError Occured at contact form endpoint -> {datetime.now()}: {error}\n===============================================\n')
            else:
                send_mail(
                    subject = "Contact Query recieved from Upwave Builders Blog!",
                    message = f"Dear {name}, \nThank you for contacting us, We have recieved your contact query and we will soon reply to your query.\nsincerely,\nUpwave Builders IT Team",
                    recipient_list=[email],
                    from_email='muhammadusman27virgo@yahoo.com'
                )
            messages.success(
                request,
                'Your contact query is submitted! We will reply back soon!',
                extra_tags='success'
            )
            return redirect('/')
        else:
            messages.warning(
                request,
                f'Your form has errors!\n{form.errors}',
                extra_tags='error'
            )
            return redirect('/contact')
    else:
        return render(
            request,
            'BlogApp/contact.html',
            {
                'form': form
            }
        )

def newsletterView(request):
    form = forms.NewsletterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            email_query = None
            try:
                email_query = models.Newsletter.objects.filter(email = form_email).first()
            except Exception as error:
                email_query = None
            if email_query is None:
                form.save()
                try:
                    send_mail(
                        subject = "Newsletter subscription, Upwave Builders",
                        message = "Thank you for subscribing to our newsletter! Now you will get the latest updates about our products, services and events. No spam, only relevant information will be shared with you.\nSincerely,\nUpwave Builders IT team",
                        from_email = "muhammadusman27virgo@yahoo.com",
                        recipient_list = [form_email]
                    )
                except Exception as error:
                    with open('logs.txt', 'a') as file:
                        file.write(f'\nError occured at newsletter endpoint -> {datetime.now()}: {error}\n')
                messages.success(
                    request,
                    'Thank you for subscribing to our newsletter!',
                    extra_tags='success'
                )
                return redirect('/')
            else:
                messages.success(
                    request,
                    'You have already subscribed our newsletter!',
                    extra_tags='success'
                )
                return redirect('/')
        else:
            messages.warning(
                request,
                'Your form has errors!',
                extra_tags='error'
            )
            return redirect('/newsletter')
    else:
        return render(
            request,
            'BlogApp/newsletter.html',
            {
                'form': form
            }
        )
        
# @login_required(login_url='/auth/login')
# def addService(request):
#     form = forms.ServicesForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             service_name = form.cleaned_data['name']
#             service_query = None
#             try:
#                 service_query = models.Services.objects.filter(name=service_name).first()
#             except Exception as error:
#                 service_query = None
#             if service_query is None:
#                 form.instance.added_by = request.user.username
#                 form.save()
#                 messages.success(
#                     request,
#                     f'Your service: {service_name} has been added to the database!'
#                 )
#                 return redirect('/')
#             else:
#                 messages.warning(
#                     request,
#                     'This service already exists in the database!'
#                 )
#                 return redirect('/')
#         else:
#             messages.warning(
#                 request,
#                 f'Your form has errors!\n{form.errors}'
#             )
#             return redirect('/add-service')
#     else:
#         return render(
#             request,
#             'BlogApp/add-service.html',
#             {
#                 'form': form
#             }
#         )
        
# def appointmentView(request):
#     form = forms.AppointmentForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             form_date = form.cleaned_data['appointment_date']
#             form_phone_number = form.cleaned_data['phone_number']
#             if form_date.weekday() in [5, 6] or form_date < date.today():
#                 messages.warning(
#                     request,
#                     'Invalid Date Selected! Kindly pick a day other than saturday or sunday'
#                 )
#                 return redirect('/appointment')
#             else:
#                 form.save()
#                 messages.success(
#                     request,
#                     'Thank you for submitting your appointment! Our correspondant will contact you soon for confirmation'
#                 )
#                 return redirect('/')
#         else:
#             messages.warning(
#                 request,
#                 f'Your form has errors!\n{form.errors}'
#             )
#             return redirect('/appointment')
#     else:
#         return render(
#             request,
#             'BlogApp/appointment.html',
#             {
#                 'form': form
#             }
#         )
        
def categoryFun():
    category_query = models.Category.objects.all().order_by('-pk')
    return category_query
        
def postView(request, slug, post_id):
    post_query = None
    try:
        post_query = models.BlogPost.objects.filter(
            title = slug.replace('-', ' '),
            pk = post_id
        ).first()
    except Exception as error:
        post_query = None
    if post_query is not None:
        return render(
            request,
            'BlogApp/post-view.html',
            {
                'post_query': post_query,
                'categories': categoryFun()
            }
        )
    else:
        messages.warning(
            request,
            'This post does not exists!',
            extra_tags='error'
        )
        return redirect('/')
    
def blogPosts(request):
    post_query = models.BlogPost.objects.all().order_by('-pk')
    pagination = Paginator(post_query, 4)
    page = request.GET.get('page')
    posts = pagination.get_page(page)
    return render(
        request,
        'BlogApp/blog-posts.html',
        {
            'posts': posts,
            'categories': categoryFun()
        }
    )
    
def categoryView(request, category):
    category_list = []
    for cat in categoryFun():
        category_list.append(cat.name)
    if category.replace('-', ' ') in category_list:
        post_query = models.BlogPost.objects.filter(category = category.replace('-', ' ')).order_by('-pk')
        pagination = Paginator(post_query, 4)
        page = request.GET.get('page')
        posts = pagination.get_page(page)
        return render(
            request,
            'BlogApp/category-view.html',
            {
                'posts': posts,
                'categories': categoryFun(),
                'category': category.replace('-', ' ')
            }
        )
    else:
        messages.warning(
            request,
            'Invalid Category Provided!',
            extra_tags='error'
        )
        return redirect('/blog-posts')
    
def searchResults(request, searched):
    post_query = models.BlogPost.objects.filter(
        content__contains = searched,
        title__contains = searched 
    ).all().order_by('-pk')
    pagination = Paginator(post_query, 4)
    page = request.GET.get('page')
    posts = pagination.get_page(page)
    return render(
        request,
        'BlogApp/search-results.html',
        {
            'posts': posts,
            'searched': searched,
            'categories': categoryFun()
        }
    )
    
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        return redirect(f'/search-results/{searched}')
    else:
        messages.warning(
            request,
            'You forgot to search!',
            extra_tags='error'
        )
        return redirect('/blog-posts')
    
def searchRedirect(request):
    messages.warning(
        request,
        'Invalid Search Operation!',
        extra_tags='error'
    )
    return redirect('/blog-posts')

def aboutView(request):
    return render(
        request,
        'BlogApp/about.html',
        {
            
        }
    )
    
def featureView(request):
    return render(
        request,
        'BlogApp/feature.html',
        {
            
        }
    )
    
def projectView(request):
    return render(
        request,
        'BlogApp/project.html',
        {
            
        }
    )
    
# def serviceView(request):
#     return render(
#         request,
#         'BlogApp/service.html',
#         {
            
#         }
#     )
    
def teamView(request):
    return render(
        request,
        'BlogApp/team.html',
        {
            
        }
    )
    
def testimonialView(request):
    return render(
        request,
        'BlogApp/testimonial.html',
        {
            
        }
    )
    
@login_required(login_url='/auth/login')
def likePost(request, post_id):
    post = get_object_or_404(
        models.BlogPost,
        id = post_id
    )
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        messages.success(
            request,
            'Post Unliked',
            extra_tags='success'
        )
        slug = post.title.replace(' ', '-')
        return redirect(f'/post-view/{slug}/{post.id}')
    else:
        post.likes.add(request.user)
        messages.success(
            request,
            'Thank you for liking this post!',
            extra_tags='success'
        )
        slug = post.title.replace(' ', '-')
        return redirect(f'/post-view/{slug}/{post.id}')