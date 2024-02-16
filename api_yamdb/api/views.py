from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthenticatedToCreateOrAuthorOrModeratorOrAdminToChangeOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
)
from .utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title


User = get_user_model()

REVIEW_IS_ONE = (
    'Пользователь не может оставить более одного отзыва '
    'на каждое произведение.'
)
USER_NOT_FOUND = 'Пользователь с никнейном {username} не найден!'
CODE_NOT_VALID = 'Неверный код подтверждения!'


class ReviewViewSet(viewsets.ModelViewSet):
    #############################################################################################################################

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedToCreateOrAuthorOrModeratorOrAdminToChangeOrReadOnly,
    )
    http_method_names = ('delete', 'get', 'patch', 'post', 'head', 'options')

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
            raise ValidationError(REVIEW_IS_ONE)
        serializer.save(author=self.request.user, title=title)
        self.update_rating()

    def perform_destroy(self, instance):
        super(ReviewViewSet, self).perform_destroy(instance)
        self.update_rating()

    def perform_update(self, serializer):
        super(ReviewViewSet, self).perform_update(serializer)
        self.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    #############################################################################################################################

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedToCreateOrAuthorOrModeratorOrAdminToChangeOrReadOnly,
    )
    http_method_names = ['delete', 'get', 'patch', 'post', 'head', 'options']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin,
                      viewsets.GenericViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
        return TitlePostSerializer


class APISignUp(CreateAPIView):
    """View-класс регистрации нового пользователя."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=request.data.get('username'))
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = serializer.save()
                user.confirmation_code = User.objects.make_random_password()
                send_confirmation_code(
                    user.email,
                    user.confirmation_code,
                    user.username
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetToken(CreateAPIView):
    """View-класс получения JWT-токена."""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {'username': USER_NOT_FOUND.format(username=username)},
                    status=status.HTTP_404_NOT_FOUND
                )
            if confirmation_code == user.confirmation_code:
                return Response(
                    {'token': str(RefreshToken.for_user(user).access_token)},
                    status=status.HTTP_200_OK
                )
        return Response(
            {'confirmation_code': CODE_NOT_VALID},
            status=status.HTTP_400_BAD_REQUEST
        )
