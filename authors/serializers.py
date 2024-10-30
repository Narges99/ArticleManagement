import re
from rest_framework import serializers
from .documents import AuthorDocument
from datetime import datetime

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

        if hasattr(instance, 'meta') and hasattr(instance.meta, 'id'):
            representation['id'] = instance.meta.id
        else:
            representation['id'] = None

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
