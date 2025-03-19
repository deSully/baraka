from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',  # Référence récursive pour les sous-catégories
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,  
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name="prices"
    )
    criterion = models.CharField(max_length=255)  # Par exemple : "taille", "quantité", "région"
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.criterion}: {self.price}"
