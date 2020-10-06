from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

# GetUsersView
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import CodeJWTView, CreateCodeViewSet, UserViewSet

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitlesViewSet,
)

router_v1 = DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("categories", CategoriesViewSet)
router_v1.register("genres", GenresViewSet)
router_v1.register("titles", TitlesViewSet)

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/api-token-auth/", views.obtain_auth_token),
    path("v1/auth/token/", CodeJWTView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/auth/email/", CreateCodeViewSet.as_view(), name="conformation_code"),
    path("v1/", include(router_v1.urls)),
]
