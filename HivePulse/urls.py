"""
URL configuration for HivePulse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import django.conf.urls as conf_urls
import BlogApp.views as blog_views

urlpatterns = [
    path('hive-pulse-admin-panel/', admin.site.urls),
    path('', include('BlogApp.urls'), name='blog-urls'),
    path('auth/', include('AuthApp.urls'), name='auth-urls'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Hive Pulse'
admin.site.index_title = 'Hive Pulse Admin Panel'
admin.site.site_title = 'CMS Admin Panel'

conf_urls.handler404 = blog_views.not_found
conf_urls.handler500 = blog_views.server_error