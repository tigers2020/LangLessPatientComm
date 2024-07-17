# article/views.py

from django.urls import reverse_lazy
from django.views.generic import DetailView

from article.models import Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'components/pages/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        # Add breadcrumbs to the context
        context['breadcrumbs'] = [
            {"name": "Home", "url": reverse_lazy('home')},
            {"name": self.object.title, "url": self.object.get_absolute_url()},
        ]

        return context
