# users/permissions.py
from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in self.allowed_roles or request.user.role == 'superadmin'
        )

class IsTeacher(RolePermission):
    allowed_roles = ['teacher']

class IsModerator(RolePermission):
    allowed_roles = ['moderator']

class IsEmployee(RolePermission):
    allowed_roles = ['employee']

class IsRegularUser(RolePermission):
    allowed_roles = ['user']
