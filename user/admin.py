from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for the custom User model."""

    # Columns visible in the user list
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_pilot",
        "is_staff_member",
        "is_staff",
        "is_superuser",
    )

    # Filters on the right
    list_filter = (
        "is_pilot",
        "is_staff_member",
        "is_staff",
        "is_superuser",
    )

    # Search fields
    search_fields = ("username", "email", "first_name", "last_name")

    # Default sorting
    ordering = ("username",)

    # Dividing fields into sections in the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {"fields": ("is_pilot", "is_staff_member")}),
    )

    # Fields available when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Information", {"fields": ("is_pilot", "is_staff_member")}),
    )
