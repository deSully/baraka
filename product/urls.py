from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryListView

router = DefaultRouter()
router.register(r'products', ProductViewSet)  # API will be available at /api/products/
router.register(r'categories', CategoryListView, basename='categories')  # API will be available at /api/categories/

urlpatterns = [
    path('', include(router.urls)),
]
