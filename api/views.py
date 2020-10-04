import random
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Categories, Genres, Review, Titles, User
from .permissions import IsAdminPerm, OwnResourcePermission, ReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitleListSerializer, TitlePostSerializer,
                          TokenSerializer, UserCodeSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [OwnResourcePermission]

    def perform_create(self, serializer):
        title = get_object_or_404(Titles,
                                  pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        review = get_object_or_404(Titles,
                                   id=self.kwargs['title_id'])
        return review.title.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission]

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CreateCodeViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            confirmation_code = ''.join(random.choices
                                        (string.ascii_uppercase +
                                         string.digits, k=30))
            User.objects.create(
                email=email, username=str(email),
                confirmation_code=confirmation_code, is_active=False
            )
            send_mail(
                f'Код регистрации для YAMDB',
                f'{confirmation_code}',
                'yamdb@yamdb.ru',
                [f'{email}'],
                fail_silently=False,
            )
            return Response({'result':
                            'Код подтверждения отправлен на почту'},
                            status=200)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CodeJWTView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.data['email'],
                    confirmation_code=serializer.data
                    ['confirmation_code']
                )

            except User is None:
                return Response(
                    data={'result': 'Юзера нет'},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh_token),
                    'token': str(refresh_token.access_token)
                })


class InfoMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self):
        return self.request.user


class GetUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCodeSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, IsAdminPerm]


class CatalogViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [IsAdminPerm | ReadOnly]
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated & IsAdminPerm | ReadOnly]


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated & IsAdminPerm | ReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('title__score'))
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated & IsAdminPerm | ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitlePostSerializer
