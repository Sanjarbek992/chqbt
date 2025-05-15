from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
from django.core.cache import cache

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    CheckPinflSerializer
)
from .models import CustomUser
from .utils import create_oauth2_tokens

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'refresh_token':
            return RefreshTokenSerializer
        elif self.action == 'profile':
            return UserProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'check_pinfl':
            return CheckPinflSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['register', 'login', 'refresh_token', 'check_pinfl']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        method='post',
        request_body=RegisterSerializer,
        responses={201: openapi.Response('Ro‘yxatdan o‘tildi')}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.raw_password = serializer.validated_data['password']
        token_data = create_oauth2_tokens(user)
        return Response({
            "message": "Foydalanuvchi yaratildi",
            "user_id": user.id,
            "token": token_data
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={200: openapi.Response('Access va Refresh token')}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # ⛔ 1. Bloklanganmi?
        if is_user_blocked(username):
            return Response({
                "detail": "Ko‘p marta noto‘g‘ri urinish! 30 daqiqadan keyin urinib ko‘ring."
            }, status=403)

        # 🔐 2. Tekshirish
        user = authenticate(username=username, password=password)

        if not user:
            attempts = increment_login_attempt(username)
            if attempts >= MAX_ATTEMPTS:
                block_user(username)
                return Response({
                    "detail": f"5 marta noto‘g‘ri urinish! Siz 30 daqiqa bloklandingiz."
                }, status=403)
            return Response({"detail": "Login yoki parol noto‘g‘ri."}, status=400)

        # ✅ 3. Urinishlar tozalansin
        reset_login_attempts(username)

        user.raw_password = password
        token_data = create_oauth2_tokens(user)

        return Response({
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
            "token_type": "Bearer"
        })

    @swagger_auto_schema(
        method='post',
        request_body=RefreshTokenSerializer,
        responses={200: openapi.Response('Yangi access token')}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='refresh-token')
    def refresh_token(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': settings.OAUTH2_CLIENT_ID,
            'client_secret': settings.OAUTH2_CLIENT_SECRET,
        }

        try:
            response = requests.post(f"{settings.BASE_OAUTH_URL}/o/token/", data=data)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @swagger_auto_schema(
        method='get',
        responses={200: UserProfileSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='profile')
    def profile(self, request):
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        responses={200: 'Logout success'}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        request.user.auth_token = None
        return Response({"message": "Tizimdan chiqildi"}, status=200)

    @swagger_auto_schema(
        method='put',
        request_body=ChangePasswordSerializer,
        responses={200: 'Parol yangilandi'}
    )
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated], url_path='change-password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not request.user.check_password(old_password):
            return Response({"detail": "Eski parol noto‘g‘ri"}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "Parol muvaffaqiyatli yangilandi"})

    @swagger_auto_schema(
        method='post',
        request_body=CheckPinflSerializer,
        responses={200: openapi.Response('PINFL mavjudligi')}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='check-pinfl')
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
