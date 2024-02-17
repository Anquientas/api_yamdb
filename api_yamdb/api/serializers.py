import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.db.models import Avg

from reviews.models import Comment, Review, Category, Genre, Title


from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import MIN_GRADE, MAX_GRADE, MAX_LENGTH_USERNAME, MAX_LENGTH_EMAIL, EXTRA_URL


User = get_user_model()

from api_yamdb.settings import LENGTH_CONFIRMATION_CODE


YEAR_MORE_CURRENT = (
    'Год выпуска {year} не может быть больше текущего {current_year}!'
)
NOT_USERNAME = 'В полученных данных отсутствует username!'
NOT_EMAIL = 'В полученных данных отсутствует email!'
USERNAME_NOT_ME = 'Использовать никнейм "me" запрещено!'

REVIEW_IS_ONE = (
    'Пользователь не может оставить более одного отзыва '
    'на каждое произведение.'
)

from reviews.validators import validate_username


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов на произведения."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = get_object_or_404(Title, id=id)
            if Review.objects.filter(author=author, title=title):
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

    # rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre',
            'rating',
        )
        read_only_fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre',
            'rating',
        )

    def validate_year(self, year):
        if year > datetime.date.today().year:
            raise serializers.ValidationError(
                YEAR_MORE_CURRENT.format(
                    year=year,
                    current_year=datetime.date.today().year
                )
            )
        return year

    # def get_rating(self, obj):
    #     average = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
    #     return int(average) if average is not None else None


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    # rating = serializers.SerializerMethodField()
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
            'rating', 'category', 'genre'
        )
        read_only_fields = ('id', 'rating')


class SignUpDataSerializer(serializers.Serializer):
    # BaseSerializer
    # Serializer
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

    # class Meta:
    #     model = User
    #     fields = ('email', 'username')

    # def validate(self, data):
    #     if 'username' not in data:
    #         raise serializers.ValidationError(
    #             {'username': NOT_USERNAME}
    #         )

    #     if 'email' not in data:
    #         raise serializers.ValidationError(
    #             {'email': NOT_EMAIL}
    #         )

    #     if User.objects.all().filter(username=data['username']):
    #         user = get_object_or_404(User, username=data['username'])
    #         if user.email != data['email']:
    #             raise serializers.ValidationError(
    #                 {'username': 'username fail'}
    #             )

    #     if User.objects.all().filter(email=data['email']):
    #         user = get_object_or_404(User, email=data['email'])
    #         if user.username != data['username']:
    #             raise serializers.ValidationError(
    #                 {'email': 'email fail'}
    #             )

    #     return data


    def create(self, validated_data):
        return User.objects.create(**validated_data)

    # def validate_username(self, username):
    #     if username == 'me':
    #         raise serializers.ValidationError(
    #             {'username': USERNAME_NOT_ME}
    #         )
    #     return username


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

    # class Meta:
    #     model = User
    #     fields = ('username', 'confirmation_code')
    #     read_only_fields = ('confirmation_code',)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


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
