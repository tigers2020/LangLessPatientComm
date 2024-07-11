# src/education/views.py

# Import necessary modules
from django.views.generic import ListView, DetailView

from .models import Scenario, Page, Choice, Outcome


# Class-based view to display multiple scenarios
class ScenarioListView(ListView):
    model = Scenario  # Model to use
    template_name = 'components/pages/education/scenario_list.html'  # Template file to use
    context_object_name = 'scenarios'  # Name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Scenarios', 'url': None}]  # current page doesn't have a URL
        return context


# Class-based view to display single scenario details
class ScenarioDetailView(DetailView):
    model = Scenario  # Model to use
    template_name = 'components/pages/education/scenario_detail.html'  # Template file to use
    context_object_name = 'scenario'  # Name to use for this model as template variable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Scenarios', 'url': '/scenarios/'},
            {'name': self.object.name, 'url': None}]  # current page doesn't have a URL
        return context


# Class-based view to display single page details
class PageDetailView(DetailView):
    model = Page  # Model to use
    template_name = 'components/pages/education/page_detail.html'  # Template file to use
    context_object_name = 'page'  # Name to use for this model as template variable


# Class-based view to display single choice details
class ChoiceDetailView(DetailView):
    model = Choice  # Model to use
    template_name = 'components/pages/education/choice_detail.html'  # Template file to use
    context_object_name = 'choice'  # Name to use for this model as template variable


# Class-based view to display single outcome details
class OutcomeDetailView(DetailView):
    model = Outcome  # Model to use
    template_name = 'components/pages/education/outcome_detail.html'  # Template file to use
    context_object_name = 'outcome'  # Name to use for this model as template variable
