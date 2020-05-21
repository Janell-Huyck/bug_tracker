from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bugs.models import CustomUser, Ticket


# help in this section is from
# https://testdriven.io/blog/django-custom-user-model/


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "tag_line",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "username",
        "first_name",
        "last_name",
        "tag_line",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "first_name", "last_name", "tag_line")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Ticket)
