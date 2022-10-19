from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """List permission for authenticated, obj permission
    for admin and author, or read only.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin)
