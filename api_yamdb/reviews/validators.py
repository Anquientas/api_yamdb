import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import USER_ENDPOINT_SUFFIX


BANNED_SYNBOL_IN_USERNAME = (
    'Никнейм "{username}" содержит неразрешенные символы:\n{symbols}'
)
USERNAME_NOT_ME = f'Использовать никнейм {USER_ENDPOINT_SUFFIX} запрещено!'
YEAR_MORE_CURRENT = (
    'Год выпуска {year} не может быть больше текущего {current_year}!'
)


def validate_username(username):
    if username == USER_ENDPOINT_SUFFIX:
        raise ValidationError(
            {'username': USERNAME_NOT_ME},
        )
    banned_symbols = re.findall(r'[^\w.@+-]', username)
    if banned_symbols:
        raise ValidationError(
            {'username': BANNED_SYNBOL_IN_USERNAME.format(
                username=username,
                symbols=''.join(set(banned_symbols))
            )},
        )
    return username
