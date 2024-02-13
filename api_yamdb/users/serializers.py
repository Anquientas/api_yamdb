from rest_framework import serializers

from .models import User


BANNED_SYMBOLS = '@.+-_'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username == 'me':
            serializers.ValidationError(
                'Использовать никнейм "me" запрещено!'
            )
        for symbol in BANNED_SYMBOLS:
            if symbol in username:
                serializers.ValidationError(
                    'Никнейм содержит недопустимый символ!'
                )
        return username
