from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Définition du schéma pour la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Baraka Product API",
        default_version="v0",
        description="Documentation de l'API pour la gestion des produits de Baraka",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="williams.stanley.desouza@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path("admin/", admin.site.urls),
    
    # Ajout des URLs des apps avec des préfixes distincts
    path("api/v0/products/", include("product.urls")),  # URLs pour les produits
    path("api/v0/orders/", include("order.urls")),  # URLs pour les commandes
    path("api/v0/merchants/", include("merchant.urls")),  # URLs pour les marchands
    # Documentation Swagger
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
]
