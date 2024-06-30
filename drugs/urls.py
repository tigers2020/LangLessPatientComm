# src/drugs/urls.py

from django.urls import path

from .views import DrugListView, DrugDetailView

urlpatterns = [
    path('', DrugListView.as_view(), name='drug_list'),
    path('<int:pk>/', DrugDetailView.as_view(), name='drug_detail'),
]
