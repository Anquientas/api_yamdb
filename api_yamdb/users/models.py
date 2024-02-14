from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .enums import UserRoles
from .validators import validate_username


class User(AbstractUser):
    """Класс пользователя."""
    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        blank=True,
        max_length=150,
        validators=(UnicodeUsernameValidator(), validate_username),
    )
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,
        blank=True,
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=True,
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=True,
        max_length=150,
    )
    bio = models.TextField(
        # verbose_name='О себе',?
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        blank=True,
        choices=UserRoles,
        default=UserRoles.USER.name
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150,
        default='1234567890'
    )

    def is_user(self):
        return self.role == UserRoles.USER.name

    def is_moderator(self):
        return self.role == UserRoles.MODERATOR.name

    def is_admin(self):
        # if self.is_staff or self.is_superuser:
        #     self.role = UserRoles.ADMIN.name
        return self.role == UserRoles.ADMIN.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # ordering = ('id',)?
        ordering = ('username',)

    def __str__(self):
        return (
            f'Никнейм: {self.username[:15]}, ',
            f'e-mail: {self.email}, ',
            f'id: {self.pk}'
        )
