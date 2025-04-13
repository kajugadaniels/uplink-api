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

class PostComment(models.Model):
    """
    Model representing a comment on a post.

    Attributes:
        post (Post): The post to which the comment is associated.
        user (User): The user who made the comment.
        comment (str): The content of the comment.
        created_at (datetime): Timestamp when the comment was created.
        updated_at (datetime): Timestamp when the comment was last updated.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', help_text="The post that this comment is associated with.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', help_text="The user who made the comment.")
    comment = models.TextField(help_text="The content of the comment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the comment was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The time when the comment was last updated.")

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

class Follow(models.Model):
    """
    Represents a following relationship between users.

    Attributes:
        follower (User): The user who follows another user.
        following (User): The user being followed.
        created_at (datetime): The timestamp when the follow relationship was created.
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_set',
        on_delete=models.CASCADE,
        help_text="User who follows another user."
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers_set',
        on_delete=models.CASCADE,
        help_text="User who is being followed."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the follow relationship was created.")

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def clean(self):
        """
        Prevent users from following themselves.
        """
        if self.follower == self.following:
            from django.core.exceptions import ValidationError
            raise ValidationError("A user cannot follow themselves.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Message(models.Model):
    """
    Represents a message exchanged between two users.

    Attributes:
        sender (User): The user who sends the message.
        receiver (User): The user who receives the message.
        body (TextField): The content of the message.
        created_at (DateTimeField): The timestamp when the message was created.
        updated_at (DateTimeField): The timestamp when the message was last updated.
        is_read (BooleanField): Indicates whether the message has been read.
        read_at (DateTimeField): The timestamp when the message was marked as read.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        help_text="User who sends the message."
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE,
        help_text="User who receives the message."
    )
    body = models.TextField(help_text="The content of the message.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the message was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the message was last updated.")
    is_read = models.BooleanField(default=False, help_text="Indicates whether the message has been read.")
    read_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the message was marked as read.")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.created_at}"