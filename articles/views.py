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
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        try:
            article = ArticleDocument.get(id=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
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
        serializer = ArticleSerializer(data=request.query_params)
        if serializer.is_valid():
            search_results = advanced_search(**serializer.validated_data)
            data = []
            for hit in search_results:
                article_dict = ArticleSerializer(hit).data
                data.append(article_dict)

            return Response({
                'count': len(data),
                'results': data
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculateCommonTagsView(APIView):
    def post(self, request, article_id):
        tags = request.data.get('tags', [])
        if not tags:
            return Response({"error": "Tags are required"}, status=status.HTTP_400_BAD_REQUEST)

        result = calculate_common_tags(article_id, tags)
        return Response(result)


class AuthorArticleCountView(APIView):
    def get(self, request):
        try:
            result = get_authors_article_count()
            return Response({
                'authors': [
                    {'name': bucket.key, 'article_count': bucket.doc_count}
                    for bucket in result
                ]
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
