from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    SignUpSerializer,
    GetTokenSerializer
)
from reviews.models import Category, Genre, Review, Title
from .utils import send_confirmation_code
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrAuthCreateOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly
)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrAuthCreateOrReadOnly,
    )
    http_method_names = ['delete', 'get', 'patch', 'post', 'head', 'options']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def update_rating(self):
        title = self.get_title()
        title.rating = int(
            title.reviews.all().aggregate(Avg('score')).get('score__avg')
        )
        title.save()

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        if Review.objects.filter(author=self.request.user, title=title):
            raise ValidationError(
                'Пользователь не может оставить более '
                'одного отзыва на каждое произведение.'
            )
        serializer.save(author=self.request.user, title=title)
        self.update_rating()

    def perform_destroy(self, instance):
        super(ReviewViewSet, self).perform_destroy(instance)
        self.update_rating()

    def perform_update(self, serializer):
        super(ReviewViewSet, self).perform_update(serializer)
        self.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrAuthCreateOrReadOnly,
    )
    http_method_names = ['delete', 'get', 'patch', 'post', 'head', 'options']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ('get', 'post', 'delete', 'head')


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ('get', 'post', 'delete', 'head')


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'delete', 'head', 'option', 'patch')


class APISignUp(APIView):
    """View-класс регистрации нового пользователя."""
    # permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.make_confirmation_code()
            send_confirmation_code(
                user.email,
                user.confirmation_code,
                user.username
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetToken(APIView):
    """View-класс получения JWT-токена."""
    # permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user = User.objects.get(username=data.get('username'))
            except User.DoesNotExist:
                return Response(
                    {'username': 'Пользователь не найден!'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if data.get('confirmation_code') == user.confirmation_code:
                token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )
