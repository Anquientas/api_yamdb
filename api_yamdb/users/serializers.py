from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()

USERNAME_NOT_ME = 'Использовать никнейм "me" запрещено!'


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'User' с правами администратора."""

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
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if 'username' in data and data['username'] == 'me':
            raise serializers.ValidationError(
                {'username': USERNAME_NOT_ME}
            )
        return data


class UserNotAdminSerializer(UserAdminSerializer):
    """Сериализатор для модели 'User' без прав администратора."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
