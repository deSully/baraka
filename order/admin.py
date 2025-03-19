from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "total_price", "status", "created_at")
    list_filter = ("status", "merchant")
    search_fields = ("merchant__name", "id")
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price_at_order")
    list_filter = ("order__status", "product")
    search_fields = ("order__id", "product__name")
    ordering = ("-order__created_at",)
