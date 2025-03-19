from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)  # API will be available at /api/products/
router.register(r'categories', CategoryViewSet)  # API will be available at /api/products/

urlpatterns = [
    path('', include(router.urls)),
]
