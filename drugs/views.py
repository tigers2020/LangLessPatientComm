from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Drug, Route, Condition


class DrugListView(ListView):
    model = Drug
    template_name = 'components/pages/drugs/drug_list.html'
    context_object_name = 'drugs'
    paginate_by = 10  # Default number of items per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters
        route_id = self.request.GET.get('route')
        use_id = self.request.GET.get('use')
        side_effect_id = self.request.GET.get('side_effect')
        search_query = self.request.GET.get('search')

        if route_id and route_id.isdigit():
            queryset = queryset.filter(route_id=int(route_id))
        if use_id and use_id.isdigit():
            queryset = queryset.filter(uses__id=int(use_id))
        if side_effect_id and side_effect_id.isdigit():
            queryset = queryset.filter(side_effects__id=int(side_effect_id))
        if search_query:
            queryset = queryset.filter(Q(brand_name__icontains=search_query) | Q(description__icontains=search_query))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items_per_page = self.request.GET.get('items_per_page', str(self.paginate_by))
        context['items_per_page'] = int(items_per_page) if items_per_page.isdigit() else self.paginate_by
        context['items_per_page_options'] = [10, 20, 50, 100, 200, 500]

        context['routes'] = Route.objects.all()
        context['uses'] = Condition.objects.all()
        context['side_effects'] = Condition.objects.filter(is_side_effect=True)

        def get_int_param(param_name):
            param_value = self.request.GET.get(param_name)
            return int(param_value) if param_value and param_value.isdigit() else 0

        context['selected_route'] = get_int_param('route')
        context['selected_use'] = get_int_param('use')
        context['selected_side_effect'] = get_int_param('side_effect')

        context['search_query'] = self.request.GET.get('search', '')

        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('items_per_page', self.paginate_by)


class DrugDetailView(DetailView):
    model = Drug
    template_name = 'components/pages/drugs/drug_detail.html'
    context_object_name = 'drug'
