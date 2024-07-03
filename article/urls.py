# article/urls.py

from django.urls import path
from . import views

app_name = 'article'  # This line adds the namespace

urlpatterns = [
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    # Add other URL patterns as needed
]