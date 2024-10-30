# authors/views.py
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ArticleSearch.settings import ELASTICSEARCH_HOST
from .documents import AuthorDocument
from .search import find_author_by_article_id
from .serializers import AuthorSerializer
from elasticsearch_dsl import Q
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[ELASTICSEARCH_HOST])

class AuthorBulkCreateView(generics.CreateAPIView):
    serializer_class = AuthorSerializer
    queryset = AuthorDocument.search()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        actions = []
        for author_data in serializer.validated_data:
            author_data['created_at'] = datetime.now()
            actions.append({
                "_op_type": "index",
                "_index": "authors",
                "_source": author_data
            })

        bulk(es, actions)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        query = Q("match_all")

        name = self.request.query_params.get("name")
        specialization = self.request.query_params.get("specialization")
        created_from = self.request.query_params.get("created_from")
        created_to = self.request.query_params.get("created_to")

        if name:
            query &= Q("match", name=name)

        if specialization:
            query &= Q("match", specialization=specialization)

        if created_from and created_to:
            query &= Q("range", created_at={"gte": created_from, "lte": created_to})

        return AuthorDocument.search().query(query)

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer

    def get_object(self):
        author_id = self.kwargs['pk']
        return AuthorDocument.get(id=author_id)

class FindAuthorByArticleView(APIView):
    def get(self, request, article_id):
        try:
            author = find_author_by_article_id(article_id)
            if author:
                serializer = AuthorSerializer(author)
                return Response(serializer.data)
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
