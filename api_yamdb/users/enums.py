from django.db.models import TextChoices


class UserRoles(TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
