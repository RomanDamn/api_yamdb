from rest_framework import serializers

from .models import Review, Comment


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
