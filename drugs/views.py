# List view for Drug model
from django.views.generic import ListView, DetailView

from .models import Drug


# List view for Drug model
class DrugListView(ListView):
    model = Drug
    template_name = 'components/pages/drugs/drug_list.html'
    context_object_name = 'drugs'
    paginate_by = 10  # Default number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_per_page'] = int(self.request.GET.get('items_per_page', self.paginate_by))
        context['items_per_page_options'] = [10, 20, 50, 100, 200, 500]  # List of options for items per page
        return context

    def get_paginate_by(self, queryset):
        # Retrieve the number of items per page from the query parameters
        return self.request.GET.get('items_per_page', self.paginate_by)


# Detail view for Drug model
class DrugDetailView(DetailView):
    model = Drug
    template_name = 'components/pages/drugs/drug_detail.html'
    context_object_name = 'drug'
