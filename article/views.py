# article/views.py

from django.urls import reverse_lazy
from django.views.generic import DetailView

from article.models import Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'components/pages/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        # Extend context with custom data
        context = super().get_context_data(**kwargs)

        # Add breadcrumb navigation
        context['breadcrumbs'] = [
            {"name": "Home", "url": reverse_lazy('home')},
            {"name": self.object.title, "url": self.object.get_absolute_url()},
        ]

        return context