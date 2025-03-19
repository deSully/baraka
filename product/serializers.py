from rest_framework import serializers
from .models import Product, Category, ProductPrice

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'criterion', 'price']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Permet d'afficher les détails de la catégorie
    prices = ProductPriceSerializer(many=True, read_only=True)  # Récupère tous les prix liés au produit

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'category', 'prices', 'created_at', 'updated_at']



class CategorysSerializer(serializers.ModelSerializer):
    parent_info = serializers.SerializerMethodField()
    subcategories_info = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_info', 'subcategories_info']

    def get_parent_info(self, obj):
        """Retourne l'ID et le nom du parent si existant."""
        if obj.parent:
            return {'id': obj.parent.id, 'name': obj.parent.name}
        return None

    def get_subcategories_info(self, obj):
        """Retourne l'ID et le nom de toutes les sous-catégories."""
        subcategories = obj.subcategories.all()
        return [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
