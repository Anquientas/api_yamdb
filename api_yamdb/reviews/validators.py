from django.core.exceptions import ValidationError

from api_yamdb.settings import EXTRA_URL


UNBANNED_SYMBOLS = '@.+-_'

BANNED_SYNBOL_IN_USERNAME = (
    'Никнейм "{username}" содержит неразрешенные символы: "{symbols}"!'
)
USERNAME_NOT_ME = f'Использовать никнейм {EXTRA_URL} запрещено!'


def validate_username(username):
    if username == EXTRA_URL:
        raise ValidationError(
            {'username': USERNAME_NOT_ME},
        )
    banned_symbols = set()
    for symbol in username:
        if not (symbol.isalnum() or UNBANNED_SYMBOLS.find(symbol) != -1):
            banned_symbols.add(symbol)

    if banned_symbols:
        raise ValidationError(
            {'username': BANNED_SYNBOL_IN_USERNAME.format(
                username=username,
                symbols=', '.join(banned_symbols)
            )},
        )
    return username
