from django.contrib import admin
from . import models
from django import forms
from django.core.validators import FileExtensionValidator
from .views import imagekit, UploadFileRequestOptions
import os
from django.conf import settings

admin.site.register(models.Contact)
admin.site.register(models.Newsletter)
admin.site.register(models.Quotation)

# custom blog post form for admin panel

# class BlogPostAdmin(admin.ModelAdmin):
#     exclude = ('slug',)

# admin.site.register(
#     models.BlogPosts,
#     BlogPostAdmin
# )

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(
    models.Category,
    CategoryAdmin
)

class AdminAddPostForm(forms.ModelForm):
    thumbnail_url = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'webp', 'jpeg', 'gif'])],
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Thumbnail for your post (optional)'
    )

    class Meta:
        model = models.BlogPosts
        fields = ('title', 'tagline', 'thumbnail_url', 'content')

class BlogPostsAdmin(admin.ModelAdmin):
    form = AdminAddPostForm
    exclude = ('slug',)
    def save_model(self, request, obj, form, change):
        if 'thumbnail_url' in form.files:
            image = form.files['thumbnail_url']
            temp_image_path = os.path.join(settings.MEDIA_ROOT, f'tempfiles/blog-thumbnail/{image.name}')
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
                        folder='/hivepulse/blog_thumbnails/'
                    )
                )
                obj.thumbnail = upload_response.url

            # Clean up the temporary file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        super().save_model(request, obj, form, change)


admin.site.register(models.BlogPosts, BlogPostsAdmin)