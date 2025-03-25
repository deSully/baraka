from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Merchant

class MerchantAdmin(UserAdmin):
    list_display = ("phone_number", "username", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
    search_fields = ("phone_number", "username", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("phone_number",)

    fieldsets = (
        (None, {"fields": ("phone_number", "username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "username", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

admin.site.register(Merchant, MerchantAdmin)
