from django.shortcuts import get_object_or_404
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins, permissions

from .models import Review
from .permissions import OwnResourcePermission
from .serializers import ReviewSerializer, CommentSerializer
import random
import string

from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.core.mail import send_mail
from rest_framework.views import APIView
from .serializers import UserCodeSerializer, TokenSerializer
from rest_framework import permissions, status, viewsets, generics
from .permissions import IsAdminPerm


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [OwnResourcePermission]
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user)


class CreateCodeViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
            User.objects.create(
                email=email, username=str(email), confirmation_code=confirmation_code, is_active=False
            )
            send_mail(
                f'Код регистрации для YAMDB',
                f'{confirmation_code}',
                'yamdb@yamdb.ru',
                [f'{email}'],
                fail_silently=False,
            )
            return Response({'result':'Код подтверждения отправлен на почту'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeJWTView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.data['email'],
                    confirmation_code=serializer.data['confirmation_code']
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
