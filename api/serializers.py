from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import User


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'pk', 'first_name', 'last_name', 'email', 'role', 'bio')
        model = User


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
