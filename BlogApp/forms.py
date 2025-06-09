# created manually!
from django import forms
from . import models
from django.core.validators import FileExtensionValidator
# from phonenumber_field.formfields import PhoneNumberField
from ckeditor.widgets import CKEditorWidget

choice_list = []
categories = models.Category.objects.all()
for category in categories:
    choice_list.append((f'{category.name}', f'{category.name}'))

# services_list = []
# services = models.Services.objects.all()
# for service in services:
#     services_list.append((f'{service.name}', f'{service.name}'))
    
# time_slots = [
#     ('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'),
#     ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
#     ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
#     ('12:00 PM - 01:00 PM', '12:00 PM - 01:00 PM'),
#     ('1:00 PM - 2:00 PM', '1:00 PM - 2:00 PM'),
#     ('2:00 PM - 3:00 PM', '2:00 PM - 3:00 PM'),
#     ('3:00 PM - 4:00 PM', '3:00 PM - 4:00 PM'),
#     ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM')
# ]

# print(services_list)

# print(choice_list)

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }
        
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
    content = CKEditorWidget(config_name="full")
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
      
class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Your name'
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Your email'
                }
            ),
            'subject': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Your subject'
                }
            ),
            'message': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'style': "height: 100px",
                    'placeholder': 'Your message Here!'
                }
            )
        }
        
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = models.Newsletter
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }
        
# class ServicesForm(forms.ModelForm):
#     class Meta:
#         model = models.Services
#         fields = (
#             'name',
#             'description'
#         )
#         widgets = {
#             'name': forms.TextInput(
#                 attrs = {
#                     'class': 'form-control'
#                 }
#             ),
#             'description': forms.Textarea(
#                 attrs = {
#                     'class': 'form-control'
#                 }
#             )
#         }
        
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = models.Appointments
#         fields = (
#             'name',
#             'email',
#             'phone_number',
#             'service',
#             'appointment_date',
#             'appointment_time',
#             'message',
#         )
#         widgets = {
#             'name': forms.TextInput(
#                 attrs = {
#                     'class': 'form-control',
#                     'placeholder': 'Your Name'
#                 }
#             ),
#             'email': forms.EmailInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Your email'
#                 }
#             ),
#             'phone_number': forms.TextInput(
#                 attrs = {
#                     'class': 'form-control',
#                     'placeholder': 'Your phone number'
#                 }
#             ),
#             'service': forms.Select(
#                 choices=services_list,
#                 attrs={
#                     'class': 'form-control form-select',
#                     'placeholder': 'Select Your Desired Service',
#                     'style': 'height: 55px;'
#                 }
#             ),
#             'appointment_date': forms.DateInput(
#                 attrs = {
#                     'class': 'form-control',
#                     'placeholder': 'Appointment Date'
#                 }
#             ),
#             'appointment_time': forms.Select(
#                 choices = time_slots,
#                 attrs = {
#                     'class': 'form-control datetimepicker-input',
#                     'placeholder': 'Time Slot',
#                     'style': 'height: 55px;'
#                 }
#             ),
#             'message': forms.Textarea(
#                 attrs = {
#                     'class': 'form-control',
#                     'placeholder': 'Your Message Here!',
#                     'rows': 5
#                 }
#             )
#         }
        
