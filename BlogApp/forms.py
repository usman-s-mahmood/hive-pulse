# created manually!
from django import forms
from . import models
from ckeditor.widgets import CKEditorWidget
from django.core.validators import FileExtensionValidator

class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            }
        ),
        label='Enter the name of category',
        required=True
    )
    class Meta:
        model = models.Category
        fields = ('name',)

class AddPostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Post Title'
            }
        ),
        label='Enter the title for your post',
        required=True
    )
    tagline = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Post Tagline'
            }
        ),
        label='Enter the tagline for your post',
        required=True
    )
    thumbnail_url = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'png', 'jpg', 'webp', 'jpeg', 'gif'
                ]
            )
        ],
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Thumbnail for your post in jpg, jpeg, png, webp or gif (optional)'
    )
    content = CKEditorWidget()
    class Meta:
        model = models.BlogPosts
        fields = (
            'title',
            'tagline',
            'thumbnail',
            'content',
        )
        label = {
            'content': 'Enter the content for your post'
        }
        
class AddServiceForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Service Name'
            }
        ),
        label='Enter the name of service',
        required=True
    )
    class Meta:
        model = models.Service
        fields = ('name',)
        
class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }
        ),
        label='Enter your name',
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }
        ),
        label='Enter your email',
        required=True
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }
        ),
        label='Enter a subject',
        required=True
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your message'
            }
        ),
        label='Enter your message',
        required=True
    )
    class Meta:
        model = models.Contact
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
    
class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }
        ),
        label='Enter your email'
    )
    class Meta:
        model = models.Newsletter
        fields = ('email',)
        
class QuotationForm(forms.ModelForm):
    name = forms.CharField(
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }
    ),
    label='Enter your name',
    required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }
        ),
        label='Enter your email',
        required=True
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your message'
            }
        ),
        label='Enter your message',
        required=True
    )
    class Meta:
        model = models.Quotation
        fields = (
            'name',
            'email',
            'message',
        )
        