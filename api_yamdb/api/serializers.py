import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Category, Genre, Title


User = get_user_model()

MIN_GRADE = 1
MAX_GRADE = 10

GRADE_IS_INT_IN_RANGE = (
    'Оценка должна быть целым числом '
    'в диапазоне от {min_grade} до {max_grade}!'
)
YEAR_MORE_CURRENT = 'Год выпуска не может быть больше текущего!'
NOT_USERNAME = 'В полученных данных отсутствует username!'
NOT_EMAIL = 'В полученных данных отсутствует email!'
USERNAME_NOT_ME = 'Использовать никнейм "me" запрещено!'
USERNAME_USE = 'Никнейм "{username}" уже используется!'
EMAIL_USE = 'Email "{email}" уже используется!'


class ReviewSerializer(serializers.ModelSerializer):
    #############################################################################################################################

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate_score(self, value):
        if value < MIN_GRADE or value > MAX_GRADE:
            raise serializers.ValidationError(
                GRADE_IS_INT_IN_RANGE.format(
                    min_grade=MIN_GRADE,
                    max_grade=MAX_GRADE
                )
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    #############################################################################################################################

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


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
    """Сериализатор произведений для метода GET."""

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(YEAR_MORE_CURRENT)
        return value


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для метода POST."""

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
        fields = '__all__'
        model = Title


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для даннных пользователя при регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(UnicodeUsernameValidator(),)
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if 'username' not in data:
            raise serializers.ValidationError(
                {'username': NOT_USERNAME}
            )
        if 'email' not in data:
            raise serializers.ValidationError(
                {'email': NOT_EMAIL}
            )
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'username': USERNAME_NOT_ME}
            )
        if User.objects.all().filter(username=data['username']):
            user = get_object_or_404(User, username=data['username'])
            if user.email != data['email']:
                raise serializers.ValidationError(
                    {'username': USERNAME_USE.format(username=user.username)}
                )
        if User.objects.all().filter(email=data['email']):
            user = get_object_or_404(User, email=data['email'])
            if user.username != data['username']:
                raise serializers.ValidationError(
                    {'email': EMAIL_USE.format(email=user.email)}
                )
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для данных пользователя при получении токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('confirmation_code',)
