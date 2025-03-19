import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    
    # Filtrage des prix via la relation avec ProductPrice
    price_min = django_filters.NumberFilter(
        field_name='prices__amount', lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='prices__amount', lookup_expr='lte'
    )

    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['name', 'category', 'price_min', 'price_max', 'stock_min']
