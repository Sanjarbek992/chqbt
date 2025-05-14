from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import UserProfile
from .serializers import RegisterSerializer, CheckPinflSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacher, IsEmployee, IsRegularUser
from .utils import create_oauth2_tokens

User = get_user_model()

class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        elif self.action == 'check_pinfl':
            return CheckPinflSerializer
        elif self.action == 'profile':
            return UserProfileSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_data = create_oauth2_tokens(user)

        return Response({
            "message": "Foydalanuvchi ro‘yxatdan o‘tdi",
            "token": token_data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='check-pinfl')
    def check_pinfl(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pinfl = serializer.validated_data['pinfl']

        if not pinfl.isdigit() or len(pinfl) != 14:
            return Response({"detail": "PINFL noto‘g‘ri formatda."}, status=400)

        exists = User.objects.filter(pinfl=pinfl).exists()
        if exists:
            return Response({"detail": "Bu PINFL allaqachon mavjud."}, status=400)

        cached = cache.get(pinfl)
        return Response({"exists": False, "from_cache": bool(cached), "data": cached})

    @action(detail=False, methods=['get', 'put'], url_path='profile', permission_classes=[IsAuthenticated])
    def profile(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.user.profile_completed = True
        request.user.save()
        return Response(serializer.data)
