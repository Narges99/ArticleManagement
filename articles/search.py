from elasticsearch_dsl import Q, A

from ArticleSearch.settings import ELASTICSEARCH_HOST
from articles.documents import ArticleDocument
from elasticsearch.client import Elasticsearch
from elasticsearch_dsl import Search

def advanced_search(keyword=None, tags=None, categories=None, author=None, start_date=None, end_date=None):
    search = ArticleDocument.search()

    if keyword:
        keyword_query = Q(
            'bool',
            should=[
                Q('match', title={
                    'query': keyword,
                    'boost': 3,
                    'operator': 'and'
                }),
                Q('match', content={
                    'query': keyword,
                    'operator': 'and'
                })
            ],
            minimum_should_match=1
        )
        search = search.query(keyword_query)

    if tags:
        if isinstance(tags, str):
            tags = [tags]
        tags_query = Q('terms', tags=tags)
        search = search.query(tags_query)

    if categories:
        if isinstance(categories, str):
            categories = [categories]
        categories_query = Q('terms', categories=categories)
        search = search.query(categories_query)

    if author:
        author_query = Q(
            'nested',
            path='author',
            query=Q('match', author__name={
                'query': author,
                'operator': 'and'
            })
        )
        search = search.query(author_query)

    if start_date and end_date:
        date_query = Q(
            'range',
            published_date={
                'gte': start_date,
                'lte': end_date
            }
        )
        search = search.query(date_query)

    search = search.sort('-published_date')

    response = search.execute()

    print(search.to_dict())

    return response

def calculate_common_tags(article_id, tags):
    client = Elasticsearch([ELASTICSEARCH_HOST])

    search = Search(using=client, index='articles').query('match_all')
    all_articles = search.execute()

    similar_articles = []
    for article in all_articles:
        if article.meta.id != article_id and hasattr(article, 'tags'):
            common_tags = [tag for tag in tags if tag in article.tags]
            if common_tags:
                similar_articles.append({
                    'article_id': article.meta.id,
                    'title': article.title,
                    'common_tags': common_tags,
                    'common_tags_count': len(common_tags)
                })

    script = {
        "script": {
            "lang": "painless",
            "source": """
                ctx._source.similar_articles = params.similar_articles;
            """,
            "params": {
                "similar_articles": similar_articles
            }
        }
    }

    try:
        result = client.update(
            index='articles',
            id=article_id,
            body=script
        )
        return {
            "article_id": article_id,
            "similar_articles": similar_articles
        }
    except Exception as e:
        print(f"Error calculating common tags: {e}")
        raise

def get_authors_article_count():
    client = Elasticsearch([ELASTICSEARCH_HOST])

    search = Search(using=client, index='articles')

    agg = A('nested', path='author')
    agg.bucket('by_author', 'terms', field='author.name.keyword', size=10)

    search.aggs.bucket('authors', agg)

    try:
        response = search.execute()
        return response.aggregations.authors.by_author.buckets
    except Exception as e:
        print(f"Error in aggregation: {e}")
        raise
