from rest_framework.permissions import BasePermission

class IsCustomAdmin(BasePermission):
    """
    Custom permission to allow only users with role='admin' or is_admin=True.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_admin)


