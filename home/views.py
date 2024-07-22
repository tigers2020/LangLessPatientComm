# File: home/views.py

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView
from article.models import Article, Category, Tag
from home.models import TeamMember, MissionContent


class HomePageView(TemplateView):
    """
    View for handling the home page.
    """
    template_name = 'components/pages/home.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the home page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)

        try:
            home_category = Category.objects.get(name="home")
            article_tag = Tag.objects.get(slug="carousel")
            articles = Article.objects.filter(tags=article_tag, category=home_category).distinct()
            context['articles'] = articles if articles.exists() else None
        except ObjectDoesNotExist:
            context['articles'] = None

        context['breadcrumbs'] = [{'name': 'Home', 'url': None}]
        return context


class EmergencyGuidelineView(TemplateView):
    """
    View for handling the emergency guideline page.
    """
    template_name = 'components/pages/emergency_contact.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the emergency guideline page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['guide'] = Article.objects.filter(category__slug='emergency', tags__slug='guide')
        context['tip'] = Article.objects.filter(category__slug='emergency', tags__slug='tip')
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Emergency Guideline', 'url': None}]
        return context


class Scanner(TemplateView):
    """
    View for handling the scanner page.
    """
    template_name = 'components/pages/ocr_app/Scanner.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the scanner page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Scanner', 'url': None}]
        return context


class PrescriptionRefillView(TemplateView):
    """
    View for handling the prescription refill page.
    """
    template_name = 'components/pages/prescription.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the prescription refill page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve or create the guide and tip objects for the context
        guide = cache.get('refill_guide')
        tip = cache.get('refill_tip')
        if not guide:
            guide = list(
                Article.objects.filter(category__slug='refill', tags__slug='guide').order_by('id').prefetch_related(
                    'tags')
            )
            cache.set('refill_guide', guide)
        if not tip:
            tip = list(
                Article.objects.filter(category__slug='refill', tags__slug='tip').order_by('id').prefetch_related(
                    'tags')
            )
            cache.set('refill_tip', tip)
        context['guide'] = guide
        context['tip'] = tip
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Prescription Refill', 'url': None}]
        return context


class AboutUsView(TemplateView):
    """
    View for handling the about us page.
    """
    template_name = 'components/pages/about_us.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the about us page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'About Us', 'url': None}]
        return context


class MissionView(ListView):
    """
    View for displaying the mission content.
    """
    model = MissionContent
    template_name = 'components/pages/mission.html'
    context_object_name = 'mission_contents'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the mission page template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [{'name': 'Home', 'url': '/'}, {'name': 'Mission', 'url': None}]
        return context
