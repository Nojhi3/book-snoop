from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow only admin users to access certain views.
    """

    def has_permission(self, request, view):
        """Check if user is authenticated and is an admin"""
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
