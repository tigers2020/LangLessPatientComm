# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from doctors.models import Doctor, Specialty


class DoctorListView(ListView):
    """
    This is a ListView for the Doctor model.
    It handles the pagination, filtering and sorting of the doctors list.
    """

    # Here we specify the model, template, context object name and default page size for the list view
    model = Doctor
    template_name = 'components/pages/doctors/doctor_list.html'
    context_object_name = 'doctors'
    default_paginate_by = 50  # Default items per page
    items_per_page_options = [10, 20, 50, 100, 200, 500]

    def get_page_size(self, queryset):
        """
        Returns the size of the page for pagination. The size is retrieved from the HTTP GET parameters if available,
        otherwise a default value is used.
        """
        return self._get_request_value('items_per_page', self.default_paginate_by)

    def get_queryset(self):
        """
        Override the get_queryset method to add ordering, filtering and searching functionalities.
        The filter and search criteria are retrieved from the HTTP GET parameters.
        """
        # First get the queryset from the superclass, then order it
        queryset = super().get_queryset().order_by('provider_last_name', 'provider_first_name')

        # Retrieve the search, gender and specialty filters from the HTTP GET parameters
        search_query = self._get_request_value('search', '')
        gender_filter = self._get_request_value('gender', '')
        specialty_filter = self._get_request_value('specialty', '')

        # Apply the filters to the queryset if they exist
        if search_query:
            queryset = queryset.filter(
                Q(provider_first_name__icontains=search_query) |
                Q(provider_last_name__icontains=search_query) |
                Q(primary_specialty__name__icontains=search_query)
            )
        if gender_filter:
            queryset = queryset.filter(gender__iexact=gender_filter)
        if specialty_filter:
            queryset = queryset.filter(primary_specialty__name__icontains=specialty_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add additional context variables needed in the template. These variables include
        pagination details, filter and search criteria and breadcrumbs for the page.
        """
        # Call the superclass implementation to get the context
        context = super().get_context_data(**kwargs)

        # Retrieve the search, gender and specialty filters and items per page from the HTTP GET parameters
        items_per_page = int(self._get_request_value('items_per_page', self.default_paginate_by))
        search_query = self._get_request_value('search', '')
        gender_filter = self._get_request_value('gender', '')
        specialty_filter = self._get_request_value('specialty', '')

        # Add these values to the context
        context['items_per_page'] = items_per_page
        context['items_per_page_options'] = self.items_per_page_options
        context['search_query'] = search_query
        context['gender_filter'] = gender_filter
        context['specialty_filter'] = specialty_filter

        # Add the list of all specialties and breadcrumbs to the context
        context['specialties'] = Specialty.objects.all()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Doctors', 'url': reverse_lazy('doctor-list')}
        ]

        # Get the queryset for the page and instantiate a Paginator object
        queryset = self.get_queryset()
        paginator = Paginator(queryset, items_per_page)
        page = self.request.GET.get('page')

        # Handle the cases where the page parameter is not an integer or is out of range
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Add the Page object to the context
        context['page_obj'] = page_obj

        return context

    def _get_request_value(self, param_name, default_value):
        """
        Utility method for getting HTTP GET parameters with a fallback default value.
        """
        return self.request.GET.get(param_name, default_value)


class DoctorDetailView(DetailView):
    """
    This is a DetailView for the Doctor model. It handles the display of a single doctor's details.
    """

    # Specify the model, template and context object name for the detail view
    model = Doctor
    template_name = 'components/pages/doctors/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add additional context variables needed in the template. This includes breadcrumbs
        for the page.
        """
        # Call the superclass implementation to get the context
        context = super().get_context_data(**kwargs)

        # Get the Doctor object for this detail view
        doctor = self.get_object()

        # Add the breadcrumbs to the context
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Doctors', 'url': reverse_lazy('doctor-list')},
            {'name': f'{doctor.provider_first_name} {doctor.provider_last_name}',
             'url': reverse_lazy('doctor-detail', args=[doctor.pk])}
        ]

        return context
