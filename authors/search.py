from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

from ArticleSearch import settings


def find_author_by_article_id(article_id):
    client = Elasticsearch([settings.ELASTICSEARCH_HOST])

    article_search = client.get(index='articles', id=article_id)

    if 'author' in article_search['_source']:
        author_name = article_search['_source']['author']['name']

        author_search = Search(using=client, index='authors')
        author_search = author_search.query('match', name=author_name)
        response = author_search.execute()

        if response.hits:
            return response.hits[0]
    return None
