# created manually!
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('add-category', views.addCategory, name='blog-add-category'),
    path('add-post', views.addPost, name='blog-add-post'),
    path('edit-post/<str:slug>/<int:post_id>', views.editPost, name='blog-edit-post'),
    path('delete-post/<int:post_id>', views.deletePost, name='blog-delete-post'),
    path('contact', views.contactView, name='blog-contact'),
    path('newsletter', views.newsletterView, name='blog-newsletter'),
    # path('add-service', views.addService, name='blog-add-service'),
    # path('appointment', views.appointmentView, name='blog-appointment'),
    path('post-view/<str:slug>/<int:post_id>', views.postView, name='blog-post-view'),
    path('blog-posts', views.blogPosts, name='blog-blog-posts'),
    path('category/<str:category>', views.categoryView, name='blog-category-view'),
    path('search', views.search, name = 'blog-search'),
    path('search-results/<str:searched>', views.searchResults, name = 'blog-search-results'),
    path('search-results/', views.searchRedirect, name='blog-search-redirect'),
    path('about', views.aboutView, name='blog-about'),
    # path('feature', views.featureView, name='blog-feature'),
    # path('project', views.projectView, name='blog-project'),
    # path('service', views.serviceView, name='blog-service'),
    # path('team', views.teamView, name='blog-team'),
    # path('testimonial', views.testimonialView, name='blog-testimonial'),
    path('like-post/<int:post_id>', views.likePost, name='blog-like-post'),
]