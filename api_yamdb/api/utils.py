from django.core.mail import send_mail


MESSAGE = (
    'Здравствуйте, {username}!\n'
    'Ваш код доступа к API_YaMDb: {confirmation_code}'
)


def send_confirmation_code(email, confirmation_code, username):
    """Функция отправки кода подтверждения на почту."""
    send_mail(
        subject='Код подтверждения',
        message=MESSAGE.format(
            username=username,
            confirmation_code=confirmation_code
        ),
        from_email=None,
        recipient_list=(email,),
        fail_silently=False
    )
