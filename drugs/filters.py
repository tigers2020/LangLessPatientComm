import django_filters
from .models import Drug

class DrugFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(field_name='openfda__brand_name', lookup_expr='icontains')
    sponsor_name = django_filters.CharFilter(field_name='sponsor_name', lookup_expr='icontains')

    class Meta:
        model = Drug
        fields = ['brand_name', 'sponsor_name']
