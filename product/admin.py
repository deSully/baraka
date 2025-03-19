from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, ProductPrice, Category

### 🔥 Inline admin pour gérer les prix directement dans l'admin
class ProductPriceInline(admin.TabularInline):  
    model = ProductPrice  
    extra = 1  # Ajoute une ligne vide pour faciliter l'ajout de nouveaux prix  
    fields = ('criteria', 'amount', 'created_at', 'updated_at')  

### 🔥 Admin pour les catégories (avec affichage hiérarchique)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'num_products')  
    search_fields = ('name',)  
    list_filter = ('parent',)  

    def num_products(self, obj):
        return obj.products.count()
    num_products.short_description = "Nombre de produits"

### 🔥 Admin pour les produits
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_price_display', 'stock', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at', 'stock')
    search_fields = ('name', 'category__name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'preview_image')

    fieldsets = (
        ("🔹 Informations générales", {
            "fields": ("name", "description", "category", "preview_image"),
        }),
        ("💰 Stock et Prix", {
            "fields": ("stock",),
        }),
        ("⏳ Dates", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    inlines = [ProductPriceInline]  # Ajout des prix en inline  

    ### 🔥 Affichage du range de prix
    def get_price_display(self, obj):
        prices = obj.prices.all()
        if prices.exists():
            min_price = min(p.amount for p in prices)
            max_price = max(p.amount for p in prices)
            return f"{min_price} - {max_price} CFA"
        return "Non défini"
    get_price_display.short_description = "Plage de prix"


    ### 🔥 Aperçu de l'image (si applicable)
    def preview_image(self, obj):
        if hasattr(obj, "image") and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="border-radius: 5px;" />')
        return "Pas d'image"
    preview_image.short_description = "Aperçu de l'image"

    ### 🔥 Empêcher la suppression des produits
    def has_delete_permission(self, request, obj=None):
        return False  

    ### 🔥 Ajout d'une action pour exporter les produits en CSV
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)

        writer.writerow(["Nom", "Catégorie", "Prix Min", "Prix Max", "Stock", "Créé le"])
        for product in queryset:
            prices = product.prices.all()
            min_price = min(p.amount for p in prices) if prices else "Non défini"
            max_price = max(p.amount for p in prices) if prices else "Non défini"
            writer.writerow([product.name, product.category, min_price, max_price, product.stock, product.created_at])

        return response

    export_as_csv.short_description = "Exporter en CSV"

