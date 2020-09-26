from django.shortcuts import get_object_or_404
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins, permissions

from .models import Review
from .permissions import OwnResourcePermission
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [OwnResourcePermission, permissions.AllowAny]
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission]

    def get_queryset(self):
        post = get_object_or_404(Review, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Review, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user)
