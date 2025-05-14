from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    pinfl = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password', 'pinfl')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos emas.")
        if len(data['pinfl']) != 14 or not data['pinfl'].isdigit():
            raise serializers.ValidationError("PINFL noto‘g‘ri formatda.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        pinfl = validated_data.pop('pinfl')
        user = User.objects.create_user(**validated_data)
        user.pinfl = pinfl
        user.save()
        return user


class CheckPinflSerializer(serializers.Serializer):
    pinfl = serializers.CharField(max_length=14)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
