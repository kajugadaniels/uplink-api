from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'username',
        'phone_number',
        'created_at',
        'edit_link',  # Display the 'Edit' link
        'delete_link'  # Display the 'Delete' link
    )
    search_fields = ('name', 'email', 'username', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    ordering = ('created_at',)

    # Display Edit link in list_display
    def edit_link(self, obj):
        change_url = reverse("admin:account_user_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', change_url)
    edit_link.short_description = "Edit"

    # Display Delete link in list_display
    def delete_link(self, obj):
        delete_url = reverse("admin:account_user_delete", args=[obj.pk])
        return format_html('<a href="{}" style="color: red;">Delete</a>', delete_url)
    delete_link.short_description = "Delete"
