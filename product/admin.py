from django.contrib import admin
from .models import Category, Product, ProductPrice


# Pour la catégorie (Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")  # Colonnes affichées dans la liste
    search_fields = ("name",)  # Permet de rechercher par le nom de la catégorie


# Pour le produit (Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reference",
        "name",
        "stock",
        "category",
        "created_at",
        "updated_at",
    )  # Colonnes affichées dans la liste
    search_fields = ("name", "reference")  # Recherche par nom et référence
    list_filter = ("category",)  # Filtrer par catégorie
    ordering = ("-created_at",)  # Trier par date de création (descendant)


# Pour le prix du produit (ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product", "criterion", "price")  # Colonnes affichées
    search_fields = ("product__name", "criterion")  # Recherche par produit et critère


# Enregistrement des modèles avec les classes Admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
