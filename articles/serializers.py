from rest_framework import serializers
from .documents import ArticleDocument
from datetime import datetime
import pytz


class ArticleAuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    published_date = serializers.DateTimeField()
    author = ArticleAuthorSerializer(required=False)
    tags = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    categories = serializers.ListField(child=serializers.CharField(max_length=100), required=False)

    def validate_published_date(self, value):
        now = datetime.now(pytz.UTC)
        if value > now:
            raise serializers.ValidationError("Publication date cannot be in the future.")
        return value

    def create(self, validated_data):
        title = validated_data.get('title')
        if ArticleDocument.search().query('term', title__keyword=title).count() > 0:
            raise serializers.ValidationError("An article with this title already exists.")

        author_data = validated_data.pop('author', {})
        tags_data = validated_data.pop('tags', [])

        article = ArticleDocument(**validated_data)

        if author_data:
            article.author = author_data
        if tags_data:
            article.tags = tags_data

        article.save()
        return article

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {
            'name': instance.author.name,
            'email': instance.author.email if hasattr(instance.author, 'email') else None
        } if hasattr(instance, 'author') and instance.author else None

        representation['tags'] = list(instance.tags) if hasattr(instance, 'tags') else []
        representation['categories'] = list(instance.categories) if hasattr(instance, 'categories') else []

        return representation

    def validate(self, data):
        filters = {key: value for key, value in data.items() if value}
        return filters
