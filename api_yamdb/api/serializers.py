from rest_framework import serializers
import datetime

from reviews.models import Category, Genre, Title


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
