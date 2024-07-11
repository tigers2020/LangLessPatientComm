from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView

from article.models import Article, Category, Tag
from home.models import TeamMember, MissionContent


class HomePageView(TemplateView):
    template_name = 'components/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            home_category = Category.objects.get(name="home")
            article_tag = Tag.objects.get(slug="carousel")

            # Correct lookup field and handle empty queryset
            articles = Article.objects.filter(tags=article_tag, category=home_category).distinct()
            if articles.exists():
                context['articles'] = articles
            else:
                context['articles'] = None
        except ObjectDoesNotExist:
            context['articles'] = None

        return context


class EmergencyGuidelineView(TemplateView):
    template_name = 'components/pages/emergency_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guide'] = Article.objects.filter(category__slug='emergency', tags__slug='guide')
        context['tip'] = Article.objects.filter(category__slug='emergency', tags__slug='tip')

        return context


class Scanner(TemplateView):
    template_name = 'components/pages/ocr_app/Scanner.html'
    pass


class PrescriptionRefillView(TemplateView):
    """
    View for handling prescription refill page.
    """
    template_name = 'components/pages/prescription.html'

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to provide context data for the template.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)

        # Import cache

        # Check if the data is already cached
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

        return context


class AboutUsView(TemplateView):
    template_name = 'components/pages/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context


class MissionView(ListView):
    model = MissionContent
    template_name = 'components/pages/mission.html'
    context_object_name = 'mission_contents'
