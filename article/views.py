from django.views.generic import DetailView

from article.models import Article


# Create your views here.


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'components/pages/article/article_detail.html'
