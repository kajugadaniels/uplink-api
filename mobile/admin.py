from mobile.models import *
from django.contrib import admin

class PostImageInline(admin.TabularInline):
    """
    Inline admin interface for PostImage.
    This allows administrators to add or edit images directly from the Post admin page.
    """
    model = PostImage
    extra = 1
    fields = ('image', 'created_at',)
    readonly_fields = ('created_at',)