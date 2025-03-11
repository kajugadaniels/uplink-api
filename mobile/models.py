from django.db import models
from base.models import *
from django.utils.text import slugify

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

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', help_text="The post to which this image is associated.")
    image = models.ImageField(upload_to='posts/', help_text="Upload an image for the post.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the image was uploaded.")

    def __str__(self):
        """
        Returns a string representation of the PostImage.
        """
        return f"Image for {self.post.title}"