# src/education/views.py

from django.views.generic import ListView, DetailView
from .models import Scenario, Page, Choice, Outcome

# Scenario Views
class ScenarioListView(ListView):
    model = Scenario
    template_name = 'components/pages/education/scenario_list.html'
    context_object_name = 'scenarios'

class ScenarioDetailView(DetailView):
    model = Scenario
    template_name = 'components/pages/education/scenario_detail.html'
    context_object_name = 'scenario'

# Page Views
class PageDetailView(DetailView):
    model = Page
    template_name = 'components/pages/education/page_detail.html'
    context_object_name = 'page'

# Choice Views
class ChoiceDetailView(DetailView):
    model = Choice
    template_name = 'components/pages/education/choice_detail.html'
    context_object_name = 'choice'

# Outcome Views
class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = 'components/pages/education/outcome_detail.html'
    context_object_name = 'outcome'
