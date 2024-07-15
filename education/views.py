from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Scenario, Page, Choice, Outcome

class ScenarioListView(ListView):
    model = Scenario
    template_name = 'components/pages/education/scenario_list.html'
    context_object_name = 'scenarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': None}  # Current page doesn't have a URL
        ]
        return context

class ScenarioDetailView(DetailView):
    model = Scenario
    template_name = 'components/pages/education/scenario_detail.html'
    context_object_name = 'scenario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': self.object.title, 'url': None}  # Current page doesn't have a URL
        ]
        return context

class PageDetailView(DetailView):
    model = Page
    template_name = 'components/pages/education/page_detail.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': page.scenario.title, 'url': reverse_lazy('scenario_detail', kwargs={'pk': page.scenario.pk})},
            {'name': f'Page {page.order}', 'url': None}  # Current page doesn't have a URL
        ]
        return context

class ChoiceDetailView(DetailView):
    model = Choice
    template_name = 'components/pages/education/choice_detail.html'
    context_object_name = 'choice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': 'Choices', 'url': None},  # Parent breadcrumb
            {'name': self.object.text, 'url': None}  # Current page doesn't have a URL
        ]
        return context

class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = 'components/pages/education/outcome_detail.html'
    context_object_name = 'outcome'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Scenarios', 'url': reverse_lazy('scenario_list')},
            {'name': 'Outcomes', 'url': None},  # Parent breadcrumb
            {'name': f'Outcome for {self.object.page}', 'url': None}  # Current page doesn't have a URL
        ]
        return context
