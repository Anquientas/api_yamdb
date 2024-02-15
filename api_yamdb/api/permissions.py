from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_staff
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_staff
        )


class IsAuthorOrModeratorOrAdminOrAuthCreateOrReadOnly(BasePermission):
    """Класс определяющий права доступа к вьюсетам следующий образом:
    создание нового объекта - доступно аутентифицированным пользователям;
    получение списка объектов - доступно всем;
    получение отдельного объекта - доступно всем;
    изменение/удаление отдельного объекта - доступно автору и персоналу.
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
            or request.user.is_staff
        )
