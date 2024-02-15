import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
# from rest_framework.serializers import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review, Category, Genre, Title


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть целым числом в диапазоне от 1 до 10!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    reviews = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=Review.objects.all()
    )
    comments = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше текущего года.'
            )
        return value

    def validate_rating(self, value):
        if value > 10:
            raise serializers.ValidationError(
                'Рейтинг не может быть больше 10.'
            )
        if value < 0:
            raise serializers.ValidationError(
                'Рейтинг не может быть меньше ноля.'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для даннных пользователя при регистрации."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator(),
        )
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if 'username' not in data:
            raise serializers.ValidationError({'username': 'username'})
        if 'email' not in data:
            raise serializers.ValidationError({'email': 'email'})
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'username': 'Использовать никнейм "me" запрещено!'}
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
