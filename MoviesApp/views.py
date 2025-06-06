from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def index(request):
    messages.success(
        request,
        'Testing Toast',
        extra_tags='success'
    )
    return render(
        request,
        'MoviesApp/index.html',
        {
            'index': True
        }
    )
    
def about(request):
    return render(
        request,
        'MoviesApp/about.html',
        {
            'about': True
        }
    )
    
def search(request):
    if request.method == 'POST':
        pass
    