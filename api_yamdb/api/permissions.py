from rest_framework import permissions


class UserIsAdmin(permissions.BasePermission):
    """
    Возвращает True если пользователь - админ.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.is_admin)


class UserIsAdminOrReadOnly(permissions.BasePermission):
    """
    Если запрос безопасный - возвращается True.
    Если пользователь - админ - True.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.is_admin)


class UserIsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Если запрос безопасный - возвращается True.
        Если пользователь авторизован - возвращается True.
        """

        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Если запрос безопасный - возвращается True.
        Если админ/модератор/автор - возвращается True.
        """
        if request.user and request.user.is_authenticated:
            if (request.user.is_staff or request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                    or request.method == 'POST'
                    and request.user.is_authenticated):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
