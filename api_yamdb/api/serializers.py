from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
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

    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        read_only_fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre'
        )
        fields = read_only_fields + ('rating',)

    def get_rating(self, obj):
        average = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return int(average) if average is not None else None


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


class UserNotAdminSerializer(UserAdminSerializer):
    """Сериализатор для модели 'User' без прав администратора."""

    class Meta(UserAdminSerializer.Meta):
        read_only_fields = ('role',)
