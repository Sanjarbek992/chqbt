from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Role

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    pinfl = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password', 'pinfl')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos emas")
        if len(data['pinfl']) != 14 or not data['pinfl'].isdigit():
            raise serializers.ValidationError("PINFL noto'g'ri formatda")
        if CustomUser.objects.filter(pinfl=data['pinfl']).exists():
            raise serializers.ValidationError("Bu PINFL allaqachon mavjud")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        pinfl = validated_data.pop('pinfl')
        role = Role.USER
        return CustomUser.objects.create_user(
            **validated_data,
            pinfl=pinfl,
            role=role
        )



class CheckPinflSerializer(serializers.Serializer):
    pinfl = serializers.CharField(
        max_length=14,
        help_text="Foydalanuvchining 14 xonali PINFL raqami"
    )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Foydalanuvchi nomi")
    password = serializers.CharField(write_only=True, help_text="Parol", style={"input_type": "password"})

    class Meta:
        swagger_schema_fields = {
            "example": {
                "username": "testuser",
                "password": "Secret123"
            }
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        help_text="Avval olingan refresh_token",
        style={"input_type": "text"}
    )

    class Meta:
        swagger_schema_fields = {
            "example": {
                "refresh_token": "f9f5d3ed1e3f45158d27a..."
            }
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Yangi parol kamida 8 ta belgidan iborat bo‘lishi kerak.")
        return value