# users/views.py
from rest_framework import viewsets, permissions
from users.models import CustomUser, UserProfile
from users.serializers import UserSerializer, ProfileSerializer
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

class UserViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchilarni ko‘rish, yaratish, tahrirlash va o‘chirish uchun API.

    Superadmin barcha foydalanuvchilarni ko‘radi,
    Admin/Moderator — faqat o‘z maktabidagilarni,
    Oddiy foydalanuvchi esa — faqat o‘zini ko‘radi.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CustomUser.objects.none()

        user = self.request.user
        if user.is_superuser or user.is_superadmin():
            return CustomUser.objects.all()
        elif user.is_admin() or user.is_moderator():
            return CustomUser.objects.filter(profile__school=user.profile.school)
        return CustomUser.objects.filter(id=user.id)

    @swagger_auto_schema(operation_description="Yangi foydalanuvchi yaratish")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Foydalanuvchini yangilash")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Foydalanuvchini o‘chirish")
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superadmin():
            raise PermissionDenied("Foydalanuvchini faqat SuperAdmin o‘chira oladi.")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if not self.request.user.is_superadmin():
            serializer.validated_data['role'] = 'user'
        serializer.save()

    def perform_update(self, serializer):
        if 'role' in serializer.validated_data:
            if not self.request.user.is_superadmin():
                raise PermissionDenied("Rolni faqat SuperAdmin o‘zgartira oladi.")
        serializer.save()


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchi profilini boshqarish API.

    Superadmin barcha profillarni ko‘radi,
    Admin/Moderator — faqat o‘z maktabidagilarni,
    Oddiy foydalanuvchi esa — faqat o‘zini ko‘radi.
    """
    queryset = UserProfile.objects.select_related('user', 'military_rank', 'school')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserProfile.objects.none()

        user = self.request.user
        if user.is_superuser or user.is_superadmin():
            return UserProfile.objects.all()
        elif user.is_admin() or user.is_moderator():
            return UserProfile.objects.filter(school=user.profile.school)
        return UserProfile.objects.filter(user=user)

    @swagger_auto_schema(operation_description="Yangi foydalanuvchi profilini yaratish")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Foydalanuvchi profilini yangilash")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Foydalanuvchi profilini o‘chirish")
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superadmin():
            raise PermissionDenied("Profilni faqat SuperAdmin o‘chira oladi.")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
