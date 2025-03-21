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
        'actions'
    )
    search_fields = ('name', 'email', 'username', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    ordering = ('created_at',)

    def actions(self, obj):
        change_url = reverse("admin:account_user_change", args=[obj.pk])
        delete_url = reverse("admin:account_user_delete", args=[obj.pk])
        return format_html(
            '<a class="button" style="margin-right: 8px;" href="{}">Edit</a>'
            '<a class="button" style="color: red;" href="{}">Delete</a>',
            change_url,
            delete_url
        )
    actions.short_description = "Actions"

    # Ensure 'actions' is an iterable and not just a method
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Add any custom actions if needed
        return actions
