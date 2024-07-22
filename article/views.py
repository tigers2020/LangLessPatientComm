# File: article/views.py

from django.urls import reverse_lazy
from django.views.generic import DetailView

from article.models import Article


class ArticleDetailView(DetailView):
    """
    View to display the details of a single article.
    """
    model = Article
    template_name = 'components/pages/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        """
        Extend context data with custom data, including breadcrumbs.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)  # Get the existing context data

        # Add breadcrumb navigation to the context
        context['breadcrumbs'] = [
            {"name": "Home", "url": reverse_lazy('home')},
            {"name": self.object.title, "url": self.object.get_absolute_url()},
        ]

        return context
