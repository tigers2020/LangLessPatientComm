from django.views.generic import DetailView

from article.models import Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'components/pages/article/article_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        # Add breadcrumbs to the context
        context['breadcrumbs'] = [
            {"name": "Home", "url": "/home/"},
            {"name": "Articles", "url": "/articles/"},
            {"name": "Article Detail", "url": "/articles/detail/"},
        ]

        return context
