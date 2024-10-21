# blog_drf/serializers.py

from rest_framework import serializers
from django.core.exceptions import ValidationError  # Import ValidationError
from .models import User, Post

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creates a new user instance with validated data."""
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except ValidationError as e:
            raise serializers.ValidationError({"username": str(e)})

        return user
    


class PostSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Post."""

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'published']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

