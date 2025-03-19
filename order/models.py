from django.db import models
from product.models import Product  # Assure-toi que Product est bien dans le même app
from merchant.models import Merchant  # Ton modèle Merchant


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.merchant} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # Empêche la suppression d’un produit s’il est dans une commande
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Sauvegarde le prix au moment de l'achat

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    def get_total_price(self):
        return self.quantity * self.price_at_order
