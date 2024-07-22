import django_filters

from .models import Drug


class DrugFilter(django_filters.FilterSet):
    """
    Defines filters for the Drug model.
    These filters can be used in views to filter Drug instances.
    """

    brand_name = django_filters.CharFilter(
        field_name='openfda__brand_name',
        lookup_expr='icontains'
    )
    # Filters drugs by brand name (case-insensitive, partial match)

    sponsor_name = django_filters.CharFilter(
        field_name='sponsor_name',
        lookup_expr='icontains'
    )

    # Filters drugs by sponsor name (case-insensitive, partial match)

    class Meta:
        model = Drug
        fields = ['brand_name', 'sponsor_name']
        # Specifies which fields are available for filtering
