from base.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.

    Features:
    - Displays 'name' and 'slug' fields in the list view.
    - Enables searching by category name.
    - The 'slug' field is read-only since it is automatically generated from the name.
    - Provides explicit Edit and Delete links for each record via a custom action_links column.
    """
    list_display = ('name', 'slug', 'action_links')
    search_fields = ('name',)
    readonly_fields = ('slug',)

    def action_links(self, obj):
        """
        Returns HTML links for editing and deleting the category.
        """
        change_url = reverse('admin:base_category_change', args=[obj.pk])
        delete_url = reverse('admin:base_category_delete', args=[obj.pk])
        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>', change_url, delete_url)
    action_links.short_description = 'Actions'
