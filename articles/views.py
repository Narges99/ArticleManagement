from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from .documents import ArticleDocument
from .serializers import ArticleSerializer
from elasticsearch.exceptions import NotFoundError
from .search import advanced_search, calculate_common_tags, get_authors_article_count
from rest_framework.views import APIView
from rest_framework.response import Response

class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleSerializer

class ArticleListView(APIView):
    def get(self, request):
        articles = ArticleDocument.search().execute()
        data = [ArticleSerializer(article).data for article in articles]
        return Response(data)

class ArticleDetailView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        try:
            article = ArticleDocument.get(id=pk)
            data = ArticleSerializer(article).data
            return Response(data)
        except NotFoundError:
            raise NotFound("Article not found.")

    def put(self, request, pk):
        try:
            article = ArticleDocument.get(id=pk)
        except NotFoundError:
            raise NotFound("Article not found.")

        serializer = ArticleSerializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            article = ArticleDocument.get(id=pk)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError:
            raise NotFound("Article not found.")

class AdvancedSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword')
        tags = request.query_params.getlist('tags')
        categories = request.query_params.getlist('categories')
        author = request.query_params.get('author')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if tags and not tags[0]:
            tags = None
        if categories and not categories[0]:
            categories = None

        try:
            search_results = advanced_search(
                keyword=keyword,
                tags=tags,
                categories=categories,
                author=author,
                start_date=start_date,
                end_date=end_date
            )

            data = []
            for hit in search_results:
                article_dict = {
                    'score': hit.meta.score,
                    'id': hit.meta.id,
                    'title': hit.title,
                    'content': hit.content,
                    'published_date': hit.published_date,
                    'tags': list(hit.tags) if hasattr(hit, 'tags') else [],
                    'categories': list(hit.categories) if hasattr(hit, 'categories') else []
                }

                if hasattr(hit, 'author') and hit.author:
                    article_dict['author'] = {
                        'name': hit.author.name,
                        'email': hit.author.email if hasattr(hit.author, 'email') else None
                    }

                data.append(article_dict)

            return Response({
                'count': len(data),
                'results': data
            })

        except Exception as e:
            return Response(
                {'error': f"Search error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CalculateCommonTagsView(APIView):
    def post(self, request, article_id):
        try:
            tags = request.data.get('tags', [])
            if not tags:
                return Response(
                    {"error": "Tags are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            print(f"Article ID: {article_id}")
            print(f"Tags: {tags}")

            result = calculate_common_tags(article_id, tags)
            return Response(result)

        except Exception as e:
            print(f"Error in view: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AuthorArticleCountView(APIView):
    def get(self, request):
        try:
            result = get_authors_article_count()
            return Response({
                'authors': [
                    {
                        'name': bucket.key,
                        'article_count': bucket.doc_count
                    }
                    for bucket in result
                ]
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
