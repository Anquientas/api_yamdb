from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL

# DEFAULT_FROM_EMAIL = 'api_yamdb@bacfend.ru'


# from_email берется из настроек проекта. По умолчанию из DEFAULT_FROM_EMAIL
# Необходимо убедиться
def send_confirmation_code(email, confirmation_code, username):
    """Функция отправки кода подтверждения на почту."""
    send_mail(
        subject='Код подтверждения',
        message=(
            f'Здравствуйте, {username}!\n'
            f'Ваш код доступа к API_YaMDb: {confirmation_code}'
        ),
        # from_email='api_yamdb@bacfend.ru',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False
    )
