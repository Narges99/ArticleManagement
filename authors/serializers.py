from elasticsearch_dsl import Q
from rest_framework import serializers
from .documents import AuthorDocument
from datetime import datetime
import re

class AuthorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    specialization = serializers.CharField(max_length=255, required=False)
    biography = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        if not re.match(r'^[\w\s]+$', value):
            raise serializers.ValidationError("Name must only contain letters.")
        return value

    def validate_specialization(self, value):
        if any(char in "!@#$%^&*()_+" for char in value):
            raise serializers.ValidationError("Specialization should not contain special characters.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = getattr(instance.meta, 'id', None)
        return representation

    def create(self, validated_data):
        validated_data['created_at'] = datetime.now()
        author = AuthorDocument(**validated_data)
        author.save()
        return validated_data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def bulk_create_actions(self):
        actions = []
        for author_data in self.validated_data:
            author_data['created_at'] = datetime.now()
            actions.append({
                "_op_type": "index",
                "_index": "authors",
                "_source": author_data
            })
        return actions

    def filter_by_params(self, query_params):
        query = Q("match_all")

        name = query_params.get("name")
        specialization = query_params.get("specialization")
        created_from = query_params.get("created_from")
        created_to = query_params.get("created_to")

        if name:
            query &= Q("match", name=name)

        if specialization:
            query &= Q("match", specialization=specialization)

        if created_from and created_to:
            query &= Q("range", created_at={"gte": created_from, "lte": created_to})

        return AuthorDocument.search().query(query)
