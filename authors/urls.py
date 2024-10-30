# authors/urls.py
from django.urls import path
from .views import AuthorBulkCreateView, AuthorListView, AuthorDetailView, FindAuthorByArticleView

urlpatterns = [
    path('create/', AuthorBulkCreateView.as_view(), name='author-create'),
    path('list/', AuthorListView.as_view(), name='author-list'),
    path('<str:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('byArticle/<str:article_id>/', FindAuthorByArticleView.as_view(), name='author-by-article'),
]
