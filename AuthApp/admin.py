from django.contrib import admin
from . import models
from .views import imagekit, UploadFileRequestOptions
import os
from django.conf import settings
from django import forms
from django.core.validators import FileExtensionValidator

class AdminProfileForm(forms.ModelForm):
    profile_pic_url = forms.ImageField(
        label='Your Profile Picture (optional)',
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.Profile
        fields = ('about_user', 'profile_pic_url', 'social_link')


class ProfileAdmin(admin.ModelAdmin):
    form = AdminProfileForm

    def save_model(self, request, obj, form, change):
        if 'profile_pic_url' in form.files:
            image = form.files['profile_pic_url']
            temp_image_path = os.path.join(settings.MEDIA_ROOT, f'tempfiles/profile-pictures/{image.name}')
            os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)

            # Save the image temporarily
            with open(temp_image_path, 'wb+') as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)

            # Upload to ImageKit.io CDN
            with open(temp_image_path, 'rb') as temp_file:
                upload_response = imagekit.upload_file(
                    file=temp_file,
                    file_name=image.name,
                    options=UploadFileRequestOptions(
                        folder='/hivepulse/profile_pictures/'
                    )
                )
                obj.profile_pic = upload_response.url

            # Clean up the temporary file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        super().save_model(request, obj, form, change)


admin.site.register(models.Profile, ProfileAdmin)


