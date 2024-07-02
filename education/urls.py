# src/education/urls.py

from django.urls import path
from .views import ScenarioListView, ScenarioDetailView, PageDetailView, ChoiceDetailView, OutcomeDetailView

urlpatterns = [
    path('', ScenarioListView.as_view(), name='scenario_list'),
    path('scenario/<int:pk>/', ScenarioDetailView.as_view(), name='scenario_detail'),
    path('page/<int:pk>/', PageDetailView.as_view(), name='page_detail'),
    path('choice/<int:pk>/', ChoiceDetailView.as_view(), name='choice_detail'),
    path('outcome/<int:pk>/', OutcomeDetailView.as_view(), name='outcome_detail'),
]
