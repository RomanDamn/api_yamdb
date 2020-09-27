from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (

    TokenRefreshView,
)
from .views import CreateCodeViewSet, CodeJWTView, InfoMeView, GetUsersView


router = DefaultRouter()
router.register('users', GetUsersView)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/auth/token/', CodeJWTView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/email/', CreateCodeViewSet.as_view(), name='conformation_code'),
    path('v1/users/me/', InfoMeView.as_view())


]