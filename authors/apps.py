from django.apps import AppConfig
from elasticsearch_dsl import connections

from ArticleSearch import settings
from .documents import AuthorDocument

class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'

    def ready(self):
        connections.create_connection(alias='default', hosts=[settings.ELASTICSEARCH_HOST])
        AuthorDocument.init()
