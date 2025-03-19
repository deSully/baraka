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
    subcategories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']
