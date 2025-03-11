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

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for the Post model.
    
    Features:
    - Displays key fields such as title, category, created_at, and updated_at.
    - Enables search by title and description.
    - Provides filters based on category and creation date.
    - Integrates PostImageInline to allow adding/editing post images directly from the post route.
    """
    list_display = ('title', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')
    inlines = [PostImageInline]