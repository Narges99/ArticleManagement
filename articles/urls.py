from django.urls import path
from .views import ArticleCreateView, ArticleListView, ArticleDetailView, AdvancedSearchView, CalculateCommonTagsView, \
    AuthorArticleCountView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('list/', ArticleListView.as_view(), name='article-list'),
    path('search/', AdvancedSearchView.as_view(), name='article-search'),
    path('<str:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('authors/count/', AuthorArticleCountView.as_view(), name='author-article-count'),
    path('<str:article_id>/calculate-common-tags/', CalculateCommonTagsView.as_view(), name='calculate-common-tags'),
]
