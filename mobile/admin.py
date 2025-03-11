from mobile.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

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
    - Displays key fields such as title, user, category, created_at, and updated_at.
    - Enables search by title, description, and user's username.
    - Provides filters based on user, category, and creation date.
    - Integrates PostImageInline to allow adding/editing post images directly from the post view.
    - Provides explicit Edit and Delete links via a custom 'action_links' column.
    """
    list_display = ('title', 'user', 'category', 'created_at', 'updated_at', 'action_links')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('user', 'category', 'created_at')
    inlines = [PostImageInline]

    def action_links(self, obj):
        """
        Returns HTML links for editing and deleting the post.
        """
        change_url = reverse('admin:mobile_post_change', args=[obj.pk])
        delete_url = reverse('admin:mobile_post_delete', args=[obj.pk])
        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>', change_url, delete_url)
    action_links.short_description = 'Actions'

# @admin.register(PostImage)
# class PostImageAdmin(admin.ModelAdmin):
#     """
#     Admin interface for the PostImage model.
    
#     Features:
#     - Displays the associated post and the image creation timestamp.
#     - Enables searching by the post title.
#     - Provides filtering by creation date.
#     """
#     list_display = ('post', 'created_at')
#     search_fields = ('post__title',)
#     list_filter = ('created_at',)