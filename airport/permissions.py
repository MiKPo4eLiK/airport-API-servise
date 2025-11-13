from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Only allows administrators to modify or delete data.
    Other users have read-only access (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view) -> object:
        # allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # only staff users can make changes
        return bool(request.user and request.user.is_staff)
