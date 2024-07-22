# File: src/education/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Scenario, Page, Choice, Outcome

class ScenarioListView(ListView):
    """
    ListView for displaying a list of Scenario instances.
    """
    model = Scenario
    template_name = 'components/pages/education/scenario_list.html'
    context_object_name = 'scenarios'

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': '#'}  # Current page URL as '#'
        ]
        return context

class ScenarioDetailView(DetailView):
    """
    DetailView for displaying a single Scenario instance.
    """
    model = Scenario
    template_name = 'components/pages/education/scenario_detail.html'
    context_object_name = 'scenario'

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': self.object.title, 'url': '#'}  # Current page URL as '#'
        ]
        return context

class PageDetailView(DetailView):
    """
    DetailView for displaying a single Page instance.
    """
    model = Page
    template_name = 'components/pages/education/page_detail.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': page.scenario.title, 'url': reverse_lazy('scenario_detail', kwargs={'pk': page.scenario.pk})},
            {'name': f'Page {page.order}', 'url': '#'}  # Current page URL as '#'
        ]
        return context

class ChoiceDetailView(DetailView):
    """
    DetailView for displaying a single Choice instance.
    """
    model = Choice
    template_name = 'components/pages/education/choice_detail.html'
    context_object_name = 'choice'

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': 'Choices', 'url': '#'},  # Parent breadcrumb URL as '#'
            {'name': self.object.text, 'url': '#'}  # Current page URL as '#'
        ]
        return context

class OutcomeDetailView(DetailView):
    """
    DetailView for displaying a single Outcome instance.
    """
    model = Outcome
    template_name = 'components/pages/education/outcome_detail.html'
    context_object_name = 'outcome'

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': 'Outcomes', 'url': '#'},  # Parent breadcrumb URL as '#'
            {'name': f'Outcome for {self.object.page}', 'url': '#'}  # Current page URL as '#'
        ]
        return context
