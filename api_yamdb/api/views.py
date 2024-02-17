from django.contrib.auth import get_user_model
from django.db.models import Avg
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
# from rest_framework.serializers import ValidationError
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
    ReviewSerializer,
    SignUpDataSerializer,
    GetTokenSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserAdminSerializer,
    UserNotAdminSerializer
)
from .utils import send_confirmation_code
from api.permissions import IsAdmin
from api_yamdb.settings import EXTRA_URL#, DEFAULT_CONFIRMATION_CODE
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


USER_NOT_FOUND = 'Пользователь с никнейном {username} не найден!'
CODE_NOT_VALID = 'Неверный код подтверждения!'
USERNAME_USE = 'Никнейм "{username}" уже используется!'
EMAIL_USE = 'Email "{email}" уже используется!'


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrIsAuthorOrModeratorOrAdminOrReadOnly,
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
    #     if Review.objects.filter(author=self.request.user, title=title):
    #         raise ValidationError(REVIEW_IS_ONE)
        serializer.save(author=self.request.user, title=title)
        self.update_rating()

    # def perform_destroy(self, instance):
    #     super(ReviewViewSet, self).perform_destroy(instance)
    #     self.update_rating()

    # def perform_update(self, serializer):
    #     super(ReviewViewSet, self).perform_update(serializer)
    #     self.update_rating()


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


class BaseViewSet(CreateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  viewsets.GenericViewSet):
    """Базовый ViewSet для категорий и жанров."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(BaseViewSet):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
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
















from django.db import IntegrityError
from api_yamdb.settings import generate_confirmation_code
from .utils import send_confirmation_code

class APISignUp(CreateAPIView):
    """View-класс регистрации нового пользователя."""

    def post(self, request):
        serializer = SignUpDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get('username')
        email = request.data.get('email')
        user_email = User.objects.all().filter(email=email)
        user_username = User.objects.all().filter(username=username)
        print(username, email)
        print('validated_data: ', serializer.validated_data)
        print('user_username: ', user_username)
        print('user_email: ', user_email)


        try:
            user, create = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = generate_confirmation_code()
        user.save()
        send_confirmation_code(user.email, user.confirmation_code, user.username)
        return Response(serializer.data, status=status.HTTP_200_OK)












        # if User.objects.all().filter(email=email):
        #     user = get_object_or_404(User, email=email)
        #     print('email ', user, DEFAULT_CONFIRMATION_CODE)
        #     if User.objects.all().filter(username=username):
        #         user_2 = get_object_or_404(User, username=username)
        #         print('email-username ', user_2, DEFAULT_CONFIRMATION_CODE)
        #         if user != user_2:
        #             print('No! email-username')
        #             return Response(status=status.HTTP_400_BAD_REQUEST)
        #     else:
        #         print('No! email')
        #         return Response(status=status.HTTP_400_BAD_REQUEST)

        







        # if User.objects.all().filter(username=username):
        #     user = get_object_or_404(User, username=username)
        #     print('username ', user)
        #     if user.email != email:
        #         return Response(status=status.HTTP_400_BAD_REQUEST)





            # if User.objects.all().filter(username=username):
            #     return Response(serializer.data, status=status.HTTP_200_OK)

        
        # if user_email and user_username and set(user_email) != set(user_username):
        #     print(user_email, user_username, set(user_email) != set(user_username))
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # if set(user_email) == set(user_username):
        #     print(set(user_email) == set(user_username))
        #     user = serializer.save()
        #     print('again: ', user)
        #     send_confirmation_code(
        #         user.email,
        #         user.confirmation_code,
        #         user.username
        #     )
        #     print('send ', user)
        #     return Response(serializer.data, status=status.HTTP_200_OK)


        
        
        # user = serializer.save()
        # print(user)
        # send_confirmation_code(
        #     user.email,
        #     user.confirmation_code,
        #     user.username
        # )
        # print('send ', user)
        # return Response(serializer.data, status=status.HTTP_200_OK)




        # if User.objects.all().filter(email=email):
        #     user = get_object_or_404(User, username=username)

        # if User.objects.all().filter(username=username):
        #     if User.objects.all().filter(email=email):
        #         return Response(serializer.data, status=status.HTTP_200_OK)

        # if User.objects.all().filter(email=email):
        #     if User.objects.all().filter(username=username):
        #         return Response(serializer.data, status=status.HTTP_200_OK)









        # if User.objects.all().filter(username=username):
        #     user = get_object_or_404(User, username=username)
        #     if user.email != email:
        #         raise ValidationError(
        #             {'username': USERNAME_USE.format(username=user.username)}
        #         )

        # if User.objects.all().filter(email=email):
        #     user = get_object_or_404(User, email=email)
        #     if user.username != username:
        #         raise ValidationError(
        #             {'email': EMAIL_USE.format(email=user.email)}
        #         )

        #     user = serializer.save()
        #     send_confirmation_code(
        #         user.email,
        #         user.confirmation_code,
        #         user.username
        #     )
        # return Response(serializer.data, status=status.HTTP_200_OK)




        # try:
        #     user = User.objects.get(username=request.data.get('username'))
        # except User.DoesNotExist:
        #     # user = get_object_or_404(User, email=request.data.get('email'))
        #     user = serializer.save()
        #     # user.confirmation_code = User.objects.make_random_password()
        #     send_confirmation_code(
        #         user.email,
        #         user.confirmation_code,
        #         user.username
        #     )
        # return Response(serializer.data, status=status.HTTP_200_OK)


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
    http_method_names = ['get', 'head', 'options', 'patch', 'post', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path=EXTRA_URL,
    )
    def user_data(self, request):
        if request.method == 'GET':
            serializer = UserAdminSerializer(request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        # if request.method == 'PATCH':
            # if request.user.is_admin:
            #     serializer = UserAdminSerializer(
            #         request.user,
            #         data=request.data,
            #         partial=True
            #     )
            # else:
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
        #     return Response(
        #         serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # return Response(status=status.HTTP_403_FORBIDDEN)
