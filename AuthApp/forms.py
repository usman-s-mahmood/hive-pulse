# created manullay!
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your registered username'
            }
        ),
        label='Your registered username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Enter your specified password'
            }
        ),
        label='Your password'
    )
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        ),
        label='Your personal Email'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }
        ),
        label='Enter your first name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }
        ),
        label='Enter your last name'
    )
    usable_password = None # for avoiding LDAP for front end users
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
        super().__init__(*args, *kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['password1'].label = 'Enter your password'
        self.fields['password2'].label = 'Confirm your password'
        self.fields['username'].label = 'Enter your username'
        
class CustomUserChangeForm(UserChangeForm):
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
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].label = 'Enter your first name'
        self.fields['last_name'].label = 'Enter your last name'
        self.fields['username'].label = 'Enter your username'
        self.fields['email'].label = 'Enter your email'
        
        self.fields['password'].label = 'Password Change form'
        self.fields['password'].help_text = 'Click Here for password <a href="/auth/edit-password">change</a>'
        
class CustomEditPasswordForm(PasswordChangeForm):
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
        self.fields['old_password'].widget.attrs['placeholder'] = 'Your Current Password'
        self.fields['old_password'].label = 'Enter your Current Password'
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Your New Password'
        self.fields['new_password1'].label = 'Enter your New Password'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['new_password2'].label = 'Confirm your New Password'
        
class DeleteConfirmation(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password before account deletion'
            }
        ),
        label='Enter your current password'
    )
    
class ProfileForm(forms.ModelForm):
    profile_pic_url = forms.ImageField(
        label='Your Profile Picture in jpg, jpeg, png, gif or webp (optional)',
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg', 'jpeg', 'png',
                    'gif', 'webp'
                ]
            )        
        ],
        widget=forms.FileInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    about_user = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'About yourself in 1000 characters'
            }
        ),
        label='Write about yourself (required)',
        required=True
    )
    social_link = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your social media handle (optional)'
            }
        ),
        label='Your social media handle (optional)',
        required=False
    )
    class Meta:
        model = models.Profile
        fields = (
            'about_user',
            'profile_pic_url',
            'social_link',
        )
        # widgets = {
        #     'about_user': forms.Textarea(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'About Yourself in 1000 characters'
        #         }
        #     ),
        #     'social_link': forms.TextInput(
        #         attrs = {
        #             'class': 'form-control'
        #         }
        #     )
        # }
        
# class CustomPasswordChangeForm(forms.ModelForm):
#     old_password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter your current password'
#             }
#         ),
#         label='Your Current Password'
#     )
#     new_password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter your new password'
#             }
#         ),
#         label = 'New password'
#     )
#     new_password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Confirm your new password'
#             }
#         ),
#         label='Confirm password'
#     )
#     class Meta:
#         model = User
#         fields = (
#             'old_password',
#             'new_password1',
#             'new_password2',
#         )

# forgot password forms

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = 'Enter your registered email'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter your new password'
        self.fields['new_password1'].label = 'Your New Password'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm your new password'
        self.fields['new_password2'].label = 'Confirm New Password'
