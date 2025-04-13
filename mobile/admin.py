from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from mobile.models import *

class PostImageInline(admin.TabularInline):
    """
    Inline admin interface for PostImage.
    This allows administrators to add or edit images directly from the Post admin page.
    """
    model = PostImage
    extra = 1
    fields = ('image', 'created_at',)
    readonly_fields = ('created_at',)

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'created_at',
        'updated_at',
        'edit_link',
        'delete_link',
    )
    search_fields = ('title', 'description', 'user__email', 'category__name')
    list_filter = ('category', 'created_at')
    ordering = ('created_at',)
    inlines = [PostImageInline]

    def edit_link(self, obj):
        change_url = reverse("admin:mobile_post_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:mobile_post_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"

# Register the PostImage model
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'created_at',
        'edit_link',
        'delete_link',
    )
    search_fields = ('post__title',)
    list_filter = ('created_at',)
    ordering = ('created_at',)

    def edit_link(self, obj):
        change_url = reverse("admin:mobile_postimage_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:mobile_postimage_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"

# Register the PostLike model
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'created_at',
        'edit_link',
        'delete_link',
    )
    search_fields = ('user__email', 'post__title')
    list_filter = ('created_at',)
    ordering = ('created_at',)

    def edit_link(self, obj):
        change_url = reverse("admin:mobile_postlike_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:mobile_postlike_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"

# Register the PostComment model
@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'created_at',
        'updated_at',
        'edit_link',
        'delete_link',
    )
    search_fields = ('user__email', 'post__title', 'comment')
    list_filter = ('created_at',)
    ordering = ('created_at',)

    def edit_link(self, obj):
        change_url = reverse("admin:mobile_postcomment_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:mobile_postcomment_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    search_fields = (
        'follower__email', 
        'following__email', 
        'follower__username', 
        'following__username'
    )
    list_filter = ('created_at',)
    ordering = ('-created_at',)
