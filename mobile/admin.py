from mobile.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from imagekit.admin import AdminImageMixin

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Add one empty form by default
    fields = ('image', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True
    ordering = ('created_at',)

class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 1  # Add one empty form by default
    readonly_fields = ('user', 'created_at')
    show_change_link = True
    ordering = ('created_at',)

class PostCommentInline(admin.StackedInline):
    model = PostComment
    extra = 1  # Add one empty form by default
    fields = ('user', 'comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True
    ordering = ('created_at',)

# Register the Post model with inlines
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
    inlines = [PostImageInline, PostLikeInline, PostCommentInline]  # Add inlines here

    def edit_link(self, obj):
        change_url = reverse("admin:mobile_post_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:mobile_post_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"

