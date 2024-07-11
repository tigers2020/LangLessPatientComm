from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Drug, Route, Condition


class DrugListView(ListView):
    """
    A Django ListView for displaying a list of Drugs.
    It handles pagination and allows filtering by route, usage, side effect and a search query.
    """
    model = Drug  # Drug model data is used
    template_name = 'components/pages/drugs/drug_list.html'  # This template will be used to render the drug list
    context_object_name = 'drugs'  # List data will be available in template as 'drugs'
    paginate_by = 10  # Default number of items per page

    def get_queryset(self):
        """
        Overriding get_queryset method to add filtering and searching functionalities.
        Filtering is done by 'route', 'use and 'side_effect' fields.
        Searching is done by 'brand_name' and 'description' fields.
        """

        # Call the superclass implementation to retrieve the initial queryset
        queryset = super().get_queryset().order_by('id', 'route', 'brand_name', 'description')

        # Retrieve the filter and search parameters from the HTTP GET parameters
        route_id = self.request.GET.get('route')
        use_id = self.request.GET.get('use')
        side_effect_id = self.request.GET.get('side_effect')
        search_query = self.request.GET.get('search')

        # Apply the filters to the queryset if they are provided
        if route_id and route_id.isdigit():
            queryset = queryset.filter(route_id=int(route_id))
        if use_id and use_id.isdigit():
            queryset = queryset.filter(uses__id=int(use_id))
        if side_effect_id and side_effect_id.isdigit():
            queryset = queryset.filter(side_effects__id=int(side_effect_id))
        if search_query:
            queryset = queryset.filter(Q(brand_name__icontains=search_query) | Q(description__icontains=search_query))

        # Return distinct results to avoid duplicates
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """
        Overriding get_context_data to add additional context variables needed in the template.
        These variables include pagination details, filter options and selected filters.
        """
        # Call the superclass implementation to get the initial context
        context = super().get_context_data(**kwargs)

        # Get the selected number of items per page from the HTTP GET parameters, or use the default
        items_per_page = self.request.GET.get('items_per_page', str(self.paginate_by))
        # Convert items_per_page to int or use default if it is not a number
        context['items_per_page'] = int(items_per_page) if items_per_page.isdigit() else self.paginate_by
        # A list of options for the number of items per page
        context['items_per_page_options'] = [10, 20, 50, 100, 200, 500]

        # Get all route, usage and side effect options and add them to the context
        context['routes'] = Route.objects.all()
        context['uses'] = Condition.objects.all()
        context['side_effects'] = Condition.objects.filter(is_side_effect=True)

        # add the breadcrumbs
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': '/'},  # link to the home page
            {'name': 'Drugs', 'url': None},  # current page, so url is None
        ]
        return context

        # Function to get integer parameters from the HTTP GET parameters
        def get_int_param(param_name):
            param_value = self.request.GET.get(param_name)
            return int(param_value) if param_value and param_value.isdigit() else 0

        # Get the selected route, use and side effect filters from the HTTP GET parameters, or use 0 as the default
        context['selected_route'] = get_int_param('route')
        context['selected_use'] = get_int_param('use')
        context['selected_side_effect'] = get_int_param('side_effect')

        # Get the search query from the HTTP GET parameters, or use an empty string as the default
        context['search_query'] = self.request.GET.get('search', '')

        return context

    def get_paginate_by(self, queryset):
        """
        Override get_paginate_by to set the number of items per page based on user selection.
        """
        return self.request.GET.get('items_per_page', self.paginate_by)


class DrugDetailView(DetailView):
    """
    A Django DetailView for displaying the details of a singular Drug instance.
    """
    model = Drug  # Drug model data is used
    template_name = 'components/pages/drugs/drug_detail.html'  # This template will be used to render the drug detail
    context_object_name = 'drug'  # The Drug instance will be available in the template as 'drug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add the breadcrumbs
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': '/'},  # link to the home page
            {'name': 'Drugs', 'url': '/drugs/'},  # link to the drug list
            {'name': self.object.brand_name, 'url': None},  # current page, so url is None
        ]
        return context
