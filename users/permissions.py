from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdmin(BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS): разрешены всем.
    - POST: разрешён аутентифицированным пользователям.
    - PUT/PATCH/DELETE: только автору или админу.
    """

    def has_permission(self, request, view):
        # Просмотр объявлений и комментариев — разрешено всем
        if request.method in SAFE_METHODS:
            return True

        # Создание — только для авторизованных
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Чтение — всем
        if request.method in SAFE_METHODS:
            return True

        # Правка/удаление — только автору или админу
        return obj.author == request.user or request.user.is_staff
