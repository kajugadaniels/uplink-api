from base.models import *
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.

    Features:
    - Displays 'name' and 'slug' fields in the list view.
    - Enables searching by category name.
    - The 'slug' field is read-only as it is automatically generated from the name.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    readonly_fields = ('slug',)
