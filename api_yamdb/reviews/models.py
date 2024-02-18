from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username
from api_yamdb.settings import (
    LENGTH_CONFIRMATION_CODE,
    MAX_VALUE_SCORE,
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_FIRSTNAME,
    MAX_LENGTH_LASTNAME,
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MIN_VALUE_SCORE
)
from api.utils import current_year


class UserRoles(models.TextChoices):
    """Enum-класс ролей пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Класс кастомного пользователя."""

    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=(validate_username,)
    )
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,
        max_length=MAX_LENGTH_EMAIL,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=True,
        max_length=MAX_LENGTH_FIRSTNAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=True,
        max_length=MAX_LENGTH_LASTNAME,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role) for role, _ in UserRoles.choices),
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=LENGTH_CONFIRMATION_CODE,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == UserRoles.ADMIN

    def __str__(self):
        return (
            f'Никнейм: {self.username[:20]}, '
            f'e-mail: {self.email}, '
            f'id: {self.pk}, '
            f'role: {self.role}'
        )


class BaseDescriptionModel(models.Model):
    """Базовый класс для классов жанра и категории."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseDescriptionModel):
    """Класс категории."""

    class Meta(BaseDescriptionModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseDescriptionModel):
    """Класс жанра."""

    class Meta(BaseDescriptionModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс произведения."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=(MaxValueValidator(limit_value=current_year),),
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseDiscussionModel(models.Model):
    """Базовый класс для классов комментария и отзыва."""
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)ss')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]


class Review(BaseDiscussionModel):
    """Класс отзыва."""

    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(MIN_VALUE_SCORE),
            MaxValueValidator(MAX_VALUE_SCORE)
        )
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta(BaseDiscussionModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(BaseDiscussionModel):
    """Класс комментария."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta(BaseDiscussionModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
