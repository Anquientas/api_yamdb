from django.contrib.auth import get_user_model
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.settings import (
    LENGTH_CONFIRMATION_CODE,
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_EMAIL
)
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username


User = get_user_model()


YEAR_MORE_CURRENT = (
    'Год выпуска {year} не может быть больше текущего {current_year}!'
)
REVIEW_IS_ONE = (
    'Пользователь не может оставить более одного отзыва '
    'на каждое произведение.'
)
USERNAME_USE = 'Пользователь с никнеймом {username} уже используется!'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов на произведения."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=get_object_or_404(
                Title, id=self.context['view'].kwargs.get('title_id')
            )
        ):
            raise serializers.ValidationError(REVIEW_IS_ONE)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для чтения."""

    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'rating', 'category', 'genre'
        )
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre'
        )

    def validate_year(self, year):
        current_year = timezone.now().year
        if year > current_year:
            raise serializers.ValidationError(YEAR_MORE_CURRENT.format(
                year=year,
                current_year=current_year
            ))
        return year


class SignUpDataSerializer(serializers.Serializer):
    """Сериализатор для даннных пользователя при регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=(validate_username,),
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL,
    )


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для данных пользователя при получении токена."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=(validate_username,),
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=LENGTH_CONFIRMATION_CODE
    )


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'User' с правами администратора."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                USERNAME_USE.format(username=username)
            )
        username = validate_username(username)
        return username


class UserNotAdminSerializer(UserAdminSerializer):
    """Сериализатор для модели 'User' без прав администратора."""

    class Meta(UserAdminSerializer.Meta):
        read_only_fields = ('role',)
