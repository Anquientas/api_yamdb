from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    GetTokenViewSet,
    UserCreateViewSet
)

from users.views import UserViewSet


auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view(),
        name='signup'
    ),
    path(
        'token/',
        GetTokenViewSet.as_view(),
        name='token'
    )
]

router_v1 = SimpleRouter()
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls))
    # path('v1/auth/', include(auth_urls)),
]
