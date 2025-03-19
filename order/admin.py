from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):  
    """Affiche les produits commandés directement dans l'admin des commandes"""
    model = OrderItem
    extra = 0  # Pas de lignes vides par défaut
    readonly_fields = ("product", "quantity", "price_at_order", "get_total_price")

    def get_total_price(self, obj):
        """Affiche le prix total par produit"""
        return f"{obj.get_total_price()} CFA"

    get_total_price.short_description = "Total par produit"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "total_price", "status", "created_at", "updated_at", "actions")
    list_filter = ("status", "created_at", "merchant")
    search_fields = ("merchant__device_id", "id")
    readonly_fields = ("total_price", "created_at", "updated_at")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)

    def actions(self, obj):
        """Ajoute des actions rapides pour changer le statut"""
        buttons = []
        if obj.status == "pending":
            buttons.append(f'<a class="button" href="/admin/orders/order/{obj.id}/mark_paid/">Marquer Payé</a>')
        if obj.status == "paid":
            buttons.append(f'<a class="button" href="/admin/orders/order/{obj.id}/mark_shipped/">Marquer Expédié</a>')
        if obj.status == "shipped":
            buttons.append(f'<a class="button" href="/admin/orders/order/{obj.id}/mark_delivered/">Marquer Livré</a>')
        return format_html(" | ".join(buttons))

    actions.allow_tags = True
    actions.short_description = "Actions rapides"

    def get_urls(self):
        """Ajoute des URLs personnalisées pour changer le statut"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path("<int:order_id>/mark_paid/", self.admin_site.admin_view(self.mark_paid)),
            path("<int:order_id>/mark_shipped/", self.admin_site.admin_view(self.mark_shipped)),
            path("<int:order_id>/mark_delivered/", self.admin_site.admin_view(self.mark_delivered)),
        ]
        return custom_urls + urls

    def mark_paid(self, request, order_id):
        """Passe une commande en statut 'paid'"""
        self._change_status(order_id, "paid", "Commande marquée comme payée")
        return self._redirect_to_order_list()

    def mark_shipped(self, request, order_id):
        """Passe une commande en statut 'shipped'"""
        self._change_status(order_id, "shipped", "Commande marquée comme expédiée")
        return self._redirect_to_order_list()

    def mark_delivered(self, request, order_id):
        """Passe une commande en statut 'delivered'"""
        self._change_status(order_id, "delivered", "Commande marquée comme livrée")
        return self._redirect_to_order_list()

    def _change_status(self, order_id, new_status, message):
        """Change le statut d'une commande et sauvegarde"""
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        self.message_user(order.merchant, message)

    def _redirect_to_order_list(self):
        """Redirige vers la liste des commandes"""
        from django.shortcuts import redirect
        return redirect("admin:orders_order_changelist")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price_at_order", "get_total_price")
    search_fields = ("order__id", "product__name")
    readonly_fields = ("order", "product", "quantity", "price_at_order", "get_total_price")

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} CFA"

    get_total_price.short_description = "Total par produit"
