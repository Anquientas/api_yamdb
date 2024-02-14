from rest_framework import serializers

from .models import User


BANNED_SYMBOLS = '@.+-_'


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'User'-администратора."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username == 'me':
            serializers.ValidationError(
                'Использовать никнейм "me" запрещено!',
                params={'username': username},
            )
        for symbol in BANNED_SYMBOLS:
            if symbol in username:
                serializers.ValidationError(
                    'Никнейм содержит недопустимый символ!',
                    params={'username': username},
                )
        return username


class UserNotAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'User'-не администратора."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, username):
        if username == 'me':
            serializers.ValidationError(
                'Использовать никнейм "me" запрещено!',
                params={'username': username},
            )
        for symbol in BANNED_SYMBOLS:
            if symbol in username:
                serializers.ValidationError(
                    'Никнейм содержит недопустимый символ!',
                    params={'username': username},
                )
        return username
