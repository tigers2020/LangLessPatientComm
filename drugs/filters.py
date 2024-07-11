import django_filters

from .models import Drug


class DrugFilter(django_filters.FilterSet):
    """
    Defines a set of filters for the 'Drug' model.
    The filters can be used to filter the instances of the model in the views.
    """

    # The 'brand_name' filter: allows filtering the Drugs by the 'brand_name' field in the 'openfda' related field.
    # The 'icontains' lookup expression is used, meaning the filter will match any Drug
    # where the 'brand_name' contains the specified value, case-insensitive.
    brand_name = django_filters.CharFilter(field_name='openfda__brand_name', lookup_expr='icontains')

    # The 'sponsor_name' filter: allows filtering the Drugs by the 'sponsor_name' field.
    # The 'icontains' lookup expression is used, meaning the filter will match any Drug where the 'sponsor_name'
    # contains the specified value, case-insensitive.
    sponsor_name = django_filters.CharFilter(field_name='sponsor_name', lookup_expr='icontains')

    class Meta:
        """
        Meta class for the DrugFilter.
        Specifies which model the filter is for and which fields should be included in the filter.
        """

        model = Drug  # The model the filters are for

        # The fields that the filter includes: 'brand_name' and 'sponsor_name'
        fields = ['brand_name', 'sponsor_name']
