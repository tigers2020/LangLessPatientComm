# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from doctors.models import Doctor


class DoctorListView(ListView):
    model = Doctor
    template_name = 'components/pages/doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 50  # Default items per page

    def get_paginate_by(self, queryset):
        return self.request.GET.get('items_per_page', self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        gender_filter = self.request.GET.get('gender', '')
        specialty_filter = self.request.GET.get('specialty', '')

        if search_query:
            queryset = queryset.filter(
                Q(provider_first_name__icontains=search_query) |
                Q(provider_last_name__icontains=search_query) |
                Q(primary_specialty__icontains=search_query)
            )

        if gender_filter:
            queryset = queryset.filter(gender__iexact=gender_filter)

        if specialty_filter:
            queryset = queryset.filter(primary_specialty__icontains=specialty_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_per_page = int(self.request.GET.get('items_per_page', self.paginate_by))
        search_query = self.request.GET.get('search', '')
        gender_filter = self.request.GET.get('gender', '')
        specialty_filter = self.request.GET.get('specialty', '')

        context['items_per_page'] = items_per_page
        context['items_per_page_options'] = [10, 20, 50, 100, 200, 500]
        context['search_query'] = search_query
        context['gender_filter'] = gender_filter
        context['specialty_filter'] = specialty_filter

        queryset = self.get_queryset()
        paginator = Paginator(queryset, items_per_page)
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj

        return context


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'components/pages/doctors/doctor_detail.html'
    context_object_name = 'doctor'


class DoctorCreateView(CreateView):
    model = Doctor
    template_name = 'components/pages/doctors/doctor_form.html'
    fields = '__all__'
    success_url = reverse_lazy('doctor-list')


class DoctorUpdateView(UpdateView):
    model = Doctor
    template_name = 'components/pages/doctors/doctor_form.html'
    fields = '__all__'
    success_url = reverse_lazy('doctor-list')


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'components/pages/doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor-list')
