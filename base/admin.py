from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from base.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'edit_link',
        'delete_link',
    )
    search_fields = ('name',)
    ordering = ('name',)

    def edit_link(self, obj):
        change_url = reverse("admin:base_category_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    def delete_link(self, obj):
        delete_url = reverse("admin:base_category_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"
