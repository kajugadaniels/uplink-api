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