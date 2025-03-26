from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product  # Import du modèle Product
from merchant.models import Merchant  # Import du modèle Merchant


class OrderItemSerializer(serializers.ModelSerializer):
    product = (
        serializers.StringRelatedField()
    )  # Affiche juste le nom du produit dans la réponse

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price_at_order"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True, read_only=True
    )  # Liste des produits dans la commande
    merchant = serializers.StringRelatedField()  # Affiche juste le nom du merchant

    class Meta:
        model = Order
        fields = [
            "id",
            "merchant",
            "total_price",
            "status",
            "created_at",
            "updated_at",
            "items",
        ]


class CreateOrderSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError(
                "La liste des produits ne peut pas être vide."
            )
        return value

    def create(self, validated_data):
        request = self.context["request"]
        merchant = request.user  # Supposons que le merchant est connecté

        order = Order.objects.create(merchant=merchant, total_price=0)

        total_price = 0
        items = []
        for item in validated_data["products"]:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Produit avec ID {product_id} introuvable."
                )

            # price_at_order = product.price  # On prend le prix actuel du produit
            price_at_order = 1000
            total_price += price_at_order * quantity

            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                price_at_order=price_at_order,
            )
            items.append(order_item)

        # Bulk create pour optimiser
        OrderItem.objects.bulk_create(items)

        # Met à jour le total de la commande
        order.total_price = total_price
        order.save()

        return order
