from elasticsearch_dsl import Document, Text, Date, connections
from datetime import datetime

from ArticleSearch import settings

connections.create_connection(alias='default', hosts=[settings.ELASTICSEARCH_HOST])

class AuthorDocument(Document):
    name = Text()
    specialization = Text()
    biography = Text()
    created_at = Date()

    class Index:
        name = 'authors'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    def save(self, **kwargs):
        self.created_at = self.created_at or datetime.now()
        return super().save(**kwargs)
