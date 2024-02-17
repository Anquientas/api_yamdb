from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthenticatedOrIsAuthorOrModeratorOrAdminOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpDataSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserAdminSerializer,
    UserNotAdminSerializer
)
from .utils import send_confirmation_code, generate_confirmation_code
from api.permissions import IsAdmin
from api_yamdb.settings import (
    USER_ENDPOINT_SUFFIX,
)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


CODE_NOT_VALID = 'Неверный код подтверждения!'


def update_and_send_new_confirmation_code(user):
    user.confirmation_code = generate_confirmation_code()
    user.save()
    send_confirmation_code(
        user.email,
        user.confirmation_code,
        user.username
    )


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrIsAuthorOrModeratorOrAdminOrReadOnly,
    )
    http_method_names = ('delete', 'get', 'patch', 'post', 'head', 'options')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrIsAuthorOrModeratorOrAdminOrReadOnly,
    )
    http_method_names = ['delete', 'get', 'patch', 'post', 'head', 'options']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class BaseCategoryGenreViewSet(CreateModelMixin,
                               DestroyModelMixin,
                               ListModelMixin,
                               viewsets.GenericViewSet):
    """Базовый ViewSet для категорий и жанров."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(BaseCategoryGenreViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'delete', 'head', 'option', 'patch')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer


class APISignUp(CreateAPIView):
    """View-класс регистрации нового пользователя."""

    def post(self, request):
        serializer = SignUpDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, create = User.objects.get_or_create(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        update_and_send_new_confirmation_code(user)
        # user.confirmation_code = generate_confirmation_code()
        # user.save()
        # send_confirmation_code(
        #     user.email,
        #     user.confirmation_code,
        #     user.username
        # )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(CreateAPIView):
    """View-класс получения JWT-токена."""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_200_OK
            )
        update_and_send_new_confirmation_code(user)
        return Response(
            {'confirmation_code': CODE_NOT_VALID},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов приложения 'users'"""

    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'head', 'options', 'patch', 'post', 'delete')

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path=USER_ENDPOINT_SUFFIX,
    )
    def user_data(self, request):
        if request.method == 'GET':
            return Response(
                UserAdminSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = UserNotAdminSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
