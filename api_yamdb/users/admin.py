from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс отображения полей модели 'User' в админке."""
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
