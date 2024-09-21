
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and an admin
        return bool(request.user and request.user.is_staff)


class IsNotAuthenticated(BasePermission):
    """
    Custom permission to only allow access to unauthenticated users.
    """
    def has_permission(self, request, view):
        # Only allow access if the user is not authenticated
        return not request.user.is_authenticated
    
    
class IsOwner(BasePermission):
    """
    Custom permission to only allow the owner of the cart to view it.
    """
    
    def has_permission(self, request, view):
        # Only allow access if the user is not authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the request user matches the user in the cart
        return obj.userid == request.user
    
class IsAdminOrOwner(BasePermission):
    """
    Custom permission to allow access to admins or the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin or the owner of the object
        return request.user.is_staff or obj.userid == request.user