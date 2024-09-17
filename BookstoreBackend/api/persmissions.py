
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and an admin
        return bool(request.user and request.user.is_staff)
