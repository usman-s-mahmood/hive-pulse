# created manually!
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('add-category', views.add_category, name='blog-add-category'),
    path('add-service', views.add_service, name='blog-add-service'),
    path('add-post', views.add_post, name='blog-add-post'),
    path('edit-post/<int:id>', views.edit_post, name='blog-edit-post'),
    path('delete-post/<int:id>', views.delete_post, name='blog-delete-post'),
    path('posts', views.blog_posts, name='blog-posts'),
    path('posts/<str:slug>', views.post_view, name='blog-post-view'),
    path('category/<str:category>', views.category_view, name='blog-category-view'),
    path('search-results/<str:query>', views.search_results, name='blog-search-results'),
    path('search', views.search, name='blog-search'),
    path('search-results/', views.search_redirect, name='blog-search-redirect'),
    path('about', views.about_view, name='blog-about-view'),
    path('contact', views.contact_view, name='blog-contact-view'),
    path('newsletter', views.newsletter_view, name='blog-newsletter-view'),
    path('quote', views.quotation_view, name='blog-quote-view'),
    path('like-post/<int:post_id>', views.like_post, name='blog-like-post-view'),
    path('hide-post/<int:post_id>', views.hide_post, name='blog-hide-post-view'),
    path('unhide-post/<int:post_id>', views.unhide_post, name='blog-unhide-post-view'),
]