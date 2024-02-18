from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Класс, определяющий необходимость аутентификации администратора
    для доступа к действиям на ресурсе.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    """
    Класс, определяющий права доступа к вьюсетам следующий образом:
    - создание нового объекта - доступно только администратору;
    - получение списка объектов - доступно всем;
    - получение отдельного объекта - доступно всем;
    - изменение/удаление отдельного объекта - доступно только администратору.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or super().has_permission(request, view)
        )


class AdminOrModeratorOrAuthorAllOrReadOnly(
    BasePermission
):
    """
    Класс, определяющий права доступа к вьюсетам следующий образом:
    - создание нового объекта - доступно аутентифицированным пользователям;
    - получение списка объектов - доступно всем;
    - получение отдельного объекта - доступно всем;
    - изменение/удаление отдельного объекта - доступно автору и персоналу.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
