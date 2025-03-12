import os
import random
from base.models import *
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

def post_image_path(instance, filename):
    """
    Generate a unique file path for a post image by appending 7 random digits 
    to the file name based on the post title.
    """
    base_filename, file_extension = os.path.splitext(filename)
    random_number = random.randint(1000000, 9999999)  # 7-digit random number
    return f'posts/post_{slugify(instance.post.title)}_{random_number}{file_extension}'

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, help_text="Select the non-staff user who created this post.", null=True, blank=True)
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

    def save(self, *args, **kwargs):
        """
        Override save to remove the existing image file from the media folder if the image is being updated.
        """
        try:
            existing = PostImage.objects.get(id=self.id)
            if existing.image and existing.image != self.image:
                if os.path.isfile(existing.image.path):
                    os.remove(existing.image.path)
        except PostImage.DoesNotExist:
            pass
        super(PostImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to ensure that when a PostImage is deleted, the associated image file is removed from the media folder.
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(PostImage, self).delete(*args, **kwargs)

class PostLike(models.Model):
    """
    Model representing a 'like' on a post.

    Attributes:
        user (User): The user who liked the post.
        post (Post): The post that was liked.
        created_at (datetime): The timestamp when the like was created.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes", help_text="The user who liked the post.")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", help_text="The post that is liked.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the like was created.")

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"

    def __str__(self):
        """
        Returns a string representation of the PostLike instance.
        """
        return f"{self.user} liked '{self.post.title}'"