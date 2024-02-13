from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GetTokenViewSet, UserViewSet, UserCreateViewSet


router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')

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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
