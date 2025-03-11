import os
import random
from base.models import *
from django.db import models
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