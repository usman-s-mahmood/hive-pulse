# created manually!
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from . import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    
class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        
class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        
class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(
        required = False,
        validators = [
          FileExtensionValidator(
              allowed_extensions=[
                  'jpg', 'jpeg', 'png', 'gif', 'webp'
              ]
          )  
        ],
        widget = forms.FileInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = models.Profile
        fields = (
            'about_user',
            'profile_pic',
            'social_link',
        )
        widgets = {
            'about_user': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'social_link': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }
        required = {
            'profile_pic': False,
            'social_link': False
        }
        
class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'