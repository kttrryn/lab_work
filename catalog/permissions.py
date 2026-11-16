from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # POST, PUT, DELETE дозволені лише адмінам (is_staff=True)
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

