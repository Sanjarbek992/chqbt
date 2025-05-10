from rest_framework.permissions import BasePermission, SAFE_METHODS

class RoleBasedPermission(BasePermission):
    """
    Foydalanuvchining roliga qarab ruxsatlarni boshqaradi.
    - SuperAdmin: barcha amallar
    - Admin: faqat o'qish (GET)
    - Moderator: faqat o'qish (GET)
    - Teacher: faqat o'ziga tegishli ma'lumotlar
    """

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.role == "Admin":
            return True  # Full access
        elif request.user.role == "Moderator":
            return True
        elif request.user.role == "User":
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == "Admin":
            return True
        elif request.user.role == "Moderator":
            if request.method in SAFE_METHODS:
                return True
            return obj.created_by == request.user
        elif request.user.role == "User":
            return request.method in SAFE_METHODS
        return False
