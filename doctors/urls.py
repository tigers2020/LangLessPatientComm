from django.urls import path
from .views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('doctor/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor/new/', DoctorCreateView.as_view(), name='doctor-create'),
    path('doctor/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('doctor/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor-delete'),
]
