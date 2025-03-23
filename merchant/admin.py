from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(UserAdmin):
    list_display = ("phone_number", "device_id", "first_name", "last_name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("phone_number", "device_id", "first_name", "last_name")
    ordering = ("-created_at",)
    
    fieldsets = (
        (None, {"fields": ("phone_number", "device_id", "activation_code")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active",)}),
        ("Important Dates", {"fields": ("created_at",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "device_id", "activation_code", "is_active"),
        }),
    )

    readonly_fields = ("created_at",)

