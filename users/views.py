from rest_framework import viewsets, permissions
from users.models import CustomUser, UserProfile
from users.serializers import UserSerializer, ProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
        if user.is_superuser or (hasattr(user, 'is_superadmin') and user.is_superadmin):
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
        if user.is_superuser or (hasattr(user, 'is_superadmin') and user.is_superadmin):
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

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
