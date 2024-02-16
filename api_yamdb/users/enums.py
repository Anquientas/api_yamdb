from django.db.models import TextChoices


class UserRoles(TextChoices):
    """Enum-класс ролей пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
