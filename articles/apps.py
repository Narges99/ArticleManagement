from django.apps import AppConfig
from elasticsearch_dsl import connections
from .documents import ArticleDocument

class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"

    def ready(self):
        connections.create_connection(alias='default', hosts=['http://localhost:9200'])
        ArticleDocument.init()