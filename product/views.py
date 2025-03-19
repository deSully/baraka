from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductPrice
from .serializers import ProductSerializer, ProductPriceSerializer, CategorysSerializer
from .models import Category
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import pagination


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = (
        "page_size"  # Permet à l'utilisateur de spécifier la taille de page
    )
    max_page_size = 100  # Taille max d'une page


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("prices").all()
    serializer_class = ProductSerializer
    http_method_names = ["get"]  # Autorise seulement GET
    # permission_classes = [IsAuthenticated]  # Si tu veux un contrôle d'accès

    # Pagination
    pagination_class = StandardResultsSetPagination
    page_size = 10  # Nombre d'éléments par page

    # Filtrage
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter  # À définir dans `filters.py`


class ProductPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]  # Autorise toutes les actions CRUD
    # permission_classes = [IsAuthenticated]  # Si besoin de contrôle d'accès


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorysSerializer
