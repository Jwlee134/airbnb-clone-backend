from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "프로필",
            {"fields": ("username", "password", "name", "email", "is_host")},
        ),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        ("날짜", {"fields": ("last_login", "date_joined"), "classes": ("collapse",)}),
    )
    list_display = ("username", "email", "name", "is_host")
