# Imported modules from django core library and article & home models
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView

from article.models import Article, Category, Tag
from home.models import TeamMember, MissionContent


# A class to handle requests for the home page
class HomePageView(TemplateView):
    template_name = 'components/pages/home.html'

    # This method is used to add additional context data to the template
    def get_context_data(self, **kwargs):
        # Calling superclass method to get existing context
        context = super().get_context_data(**kwargs)

        # Attempt to retrieve specific articles for the home page from the database
        try:
            home_category = Category.objects.get(name="home")
            article_tag = Tag.objects.get(slug="carousel")

            # Filtering articles based on article_tag and home_category
            articles = Article.objects.filter(tags=article_tag, category=home_category).distinct()

            # Check if articles exist and update the context or set to None if not
            if articles.exists():
                context['articles'] = articles
            else:
                context['articles'] = None
        except ObjectDoesNotExist:
            context['articles'] = None
        context['breadcrumbs'] = [{'name': 'Home', 'url': None}]  # No URL for the home page since it's the current page

        # Returning the updated context
        return context


# A class to handle requests for the EmergencyGuidelineView page
class EmergencyGuidelineView(TemplateView):
    template_name = 'components/pages/emergency_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Setting guide and tip context from articles filtered by category slug and tag slug
        context['guide'] = Article.objects.filter(category__slug='emergency', tags__slug='guide')
        context['tip'] = Article.objects.filter(category__slug='emergency', tags__slug='tip')
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Emergency Guideline', 'url': None}]

        return context


class Scanner(TemplateView):
    template_name = 'components/pages/ocr_app/Scanner.html'
    # There are no additional methods or attributes here, so 'pass' is used
    pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Scanner', 'url': None}]
        return context


class PrescriptionRefillView(TemplateView):
    """
    View for handling prescription refill page.
    """
    template_name = 'components/pages/prescription.html'

    # Method to gather additional context data for the template
    def get_context_data(self, **kwargs):
        """
        Override get_context_data to provide context data for the template.
        Returns:
            dict: Context data for the template.
        """
        # Calling superclass method to get existing context
        context = super().get_context_data(**kwargs)

        # Retrieve or create the guide and tip objects for the context
        guide = cache.get('refill_guide')
        tip = cache.get('refill_tip')
        if not guide:
            guide = list(
                Article.objects.filter(category__slug='refill', tags__slug='guide').order_by('id').prefetch_related(
                    'tags'))
            cache.set('refill_guide', guide)
        if not tip:
            tip = list(
                Article.objects.filter(category__slug='refill', tags__slug='tip').order_by('id').prefetch_related(
                    'tags'))
            cache.set('refill_tip', tip)
        context['guide'] = guide
        context['tip'] = tip
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Prescription Refill', 'url': None}]

        # Returning the updated context
        return context


class AboutUsView(TemplateView):
    template_name = 'components/pages/about_us.html'

    def get_context_data(self, **kwargs):
        # Calling superclass method to get existing context
        context = super().get_context_data(**kwargs)

        # Providing all TeamMembers objects for the 'team_members' context variable
        context['team_members'] = TeamMember.objects.all()
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'About Us', 'url': None}]

        # Returning the updated context
        return context


class MissionView(ListView):
    model = MissionContent
    template_name = 'components/pages/mission.html'
    context_object_name = 'mission_contents'

    # Display content about the organization's mission
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Mission', 'url': None}]
        return context
