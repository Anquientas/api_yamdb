from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .enums import UserRoles


class User(AbstractUser):
    """Класс кастомного пользователя."""

    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        blank=True,
        max_length=150,
        validators=(UnicodeUsernameValidator(),),
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
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=10,
        default='1234567890'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # ordering = ('id',)?
        ordering = ('username',)

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_admin(self):
        if self.is_staff and self.role != UserRoles.ADMIN:
            self.role = UserRoles.ADMIN
        return self.role == UserRoles.ADMIN

    def __str__(self):
        return (
            f'Никнейм: {self.username[:15]}, '
            f'e-mail: {self.email}, '
            f'id: {self.pk}'
            f'role: {self.role}'
        )
