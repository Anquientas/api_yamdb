import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
# from rest_framework.serializers import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Category, Genre, Title

from django.shortcuts import get_object_or_404


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

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для даннных пользователя при регистрации."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            # UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator(),
        )
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        # validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if 'username' not in data:
            raise serializers.ValidationError({'username': 'username не поступил с данными!'})
        if 'email' not in data:
            raise serializers.ValidationError({'email': 'email не поступил с данными!'})
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'username': 'Использовать никнейм "me" запрещено!'}
            )
        if User.objects.all().filter(username=data['username']):
            user = get_object_or_404(User, username=data['username'])
            if user.email != data['email']:
                raise serializers.ValidationError({'username': 'Такой никнейм уже использован!'})

        if User.objects.all().filter(email=data['email']):
            user = get_object_or_404(User, email=data['email'])
            if user.username != data['username']:
                raise serializers.ValidationError({'email': 'Такой email уже использован!'})

        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для данных пользователя при получении токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('confirmation_code',)
