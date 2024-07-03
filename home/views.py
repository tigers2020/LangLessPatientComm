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
    template_name = 'components/pages/Scanner.html'
    pass

class PrescriptionRefillView(TemplateView):
    template_name = 'components/pages/prescription.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch articles in reverse order by id
        context['guide'] = Article.objects.filter(category__slug='refill', tags__slug='guide').order_by('-id')
        context['tip'] = Article.objects.filter(category__slug='refill', tags__slug='tip').order_by('-id')

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
