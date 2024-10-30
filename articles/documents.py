from elasticsearch_dsl import Document, Text, Date, Keyword, Nested, InnerDoc, connections
from ArticleSearch import settings

connections.create_connection(alias='default', hosts=[settings.ELASTICSEARCH_HOST])

class Author(InnerDoc):
    name = Text(fields={'keyword': Keyword()})
    email = Text()

class ArticleDocument(Document):
    title = Text()
    content = Text()
    published_date = Date()
    author = Nested(Author)
    tags = Keyword(multi=True)
    categories = Keyword(multi=True)

    class Index:
        name = 'articles'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    def save(self, **kwargs):
        self.published_date = self.published_date or Date.now()
        return super().save(**kwargs)
