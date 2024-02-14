from django.core.exceptions import ValidationError


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            ('Использовать никнейм "me" запрещено!'),
            params={'username': username},
        )
