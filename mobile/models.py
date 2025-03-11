import os
from base.models import *
from django.db import models
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

class Post(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the title of the post.")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', help_text="Select the category for the post.")
    description = models.TextField(help_text="Enter the content or description of the post.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the post was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the post was last updated.")

    def __str__(self):
        """
        Returns a string representation of the Post.
        """
        return self.title

def post_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'posts/post_{slugify(instance.post.title)}{file_extension}'

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', help_text="The post to which this image is associated.")
    image = ProcessedImageField(
        upload_to=post_image_path,
        processors=[ResizeToFill(1270, 1270)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the image was uploaded.")

    def __str__(self):
        """
        Returns a string representation of the PostImage.
        """
        return f"Image for {self.post.title}"