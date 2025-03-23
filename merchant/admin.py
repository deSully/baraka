from django.contrib import admin
from .models import Merchant

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ("phone_number","activation_code", "device_id", "is_active", "created_at")
    search_fields = ("phone_number", "device_id")
