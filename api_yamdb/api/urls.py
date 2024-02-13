from django.urls import path, include, path
from rest_framework import routers
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


api_v1_router = routers.DefaultRouter()
api_v1_router.register('categories', CategoryViewSet, basename='categories')
api_v1_router.register('genres', GenreViewSet, basename='genres')
api_v1_router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
]
