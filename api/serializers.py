from rest_framework import serializers

from .models import User, Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'pk', 'first_name', 'last_name', 'email', 'role', 'bio')
        model = User


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
