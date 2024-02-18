import datetime

from django.core.mail import send_mail

from api_yamdb.settings import FROM_EMAIL


MESSAGE = (
    'Здравствуйте, {username}!\n'
    'Ваш код доступа к API_YaMDb: {confirmation_code}'
)


def generate_confirmation_code(length=LENGTH_CONFIRMATION_CODE):
    """Функция генерации кода доступа."""

    return ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=length
    ))


def send_confirmation_code(email, confirmation_code, username):
    """Функция отправки кода подтверждения на почту."""
    send_mail(
        subject='Код подтверждения',
        message=MESSAGE.format(
            username=username,
            confirmation_code=confirmation_code
        ),
        from_email=FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False
    )


def current_year():
    return datetime.date.today().year
