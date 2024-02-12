from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Класс пользователя."""
    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=150,
        # Вынести в validators?
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Никнейм содержит недопустимый символ!'
        )]   
    )
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        # verbose_name='О себе',?
        verbose_name='Биография',
        blank=True
    )
    # ENUM? What and how?   Enum: "user" "moderator" "admin"
    role = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # ordering = ('id',)?
        ordering = ('username',)
