from base.models import *
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.

    Features:
    - Displays 'name' and 'slug' fields in the list view.
    - Enables searching by category name.
    - Automatically prepopulates the slug field based on the name.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
