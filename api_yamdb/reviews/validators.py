import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import EXTRA_URL

# YEAR_MORE_CURRENT = (
#     'Год выпуска {year} не может быть больше текущего {current_year}!'
# )


# EXTRA_URL = 'me'


UNBANNED_SYMBOLS = '@.+-_'
USERNAME_NOT_ME = f'Использовать никнейм {EXTRA_URL} запрещено!'
BANNED_SYNBOL_IN_USERNAME = (
    'Никнейм "{username}" содержит неразрешенные символы: "{symbols}"!'
)


def validate_username(username):
    if username == EXTRA_URL:
        raise ValidationError(
            {'username': USERNAME_NOT_ME},
        )
    banned_symbols = []
    for symbol in username:
        if not (symbol.isalnum() or UNBANNED_SYMBOLS.find(symbol) != -1):
            if symbol not in banned_symbols:
                banned_symbols.append(symbol)

    if banned_symbols:
        raise ValidationError(
            {'username': BANNED_SYNBOL_IN_USERNAME.format(
                username=username,
                symbols=', '.join(banned_symbols)
            )},
        )
    return username


# print(validate_username('usernam43+t'))
# print(validate_username('usern@am4_3t'))
# # print(validate_username('usern#am&43t'))
# # print(validate_username('use@rna^m43t'))
# print(validate_username('userna//634621)*&$^%^m43t'))



# def validate_year(self, year):
#     if year > datetime.date.today().year:
#         raise ValidationError(
#             YEAR_MORE_CURRENT.format(
#                 year=year,
#                 current_year=datetime.date.today().year
#             )
#         )
#     return year
