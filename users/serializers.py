from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile, Role, MilitaryRank
from egov_api.models.teacher_models import Teacher
from egov_api.models.school_models import School
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    pinfl = serializers.CharField(max_length=14)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Parollar mos emas!")

        if CustomUser.objects.filter(pinfl=data["pinfl"]).exists():
            raise serializers.ValidationError(
                "Bu PINFL bilan foydalanuvchi ro'yxatdan o'tgan!"
            )

        teacher = Teacher.objects.filter(pinfl=data["pinfl"]).first()
        data["teacher"] = teacher
        return data

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        pinfl = validated_data["pinfl"]
        teacher = validated_data["teacher"]

        role = Role.TEACHER if teacher else Role.USER
        first_name = teacher.first_name if teacher else "Ismi"
        last_name = teacher.last_name if teacher else "Familiyasi"

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            pinfl=pinfl,
            role=role,
            password=password,
        )

        if not hasattr(user, "profile"):
            if teacher:
                UserProfile.objects.create(
                    user=user,
                    middle_name=teacher.middle_name,
                    birth_date=teacher.birth_date,
                    gender=teacher.gender,
                    passport_series=teacher.document_series,
                    passport_number=teacher.document_number,
                    oblast=teacher.oblast,
                    region=teacher.region,
                    school=teacher.school,
                    organization_name=teacher.organisation_name,
                    position_name=teacher.position_name,
                )
            else:
                UserProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "token_type": "Bearer",
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and not request.user.is_superuser:
            for field in [
                "school",
                "passport_series",
                "passport_number",
                "oblast",
                "region",
            ]:
                if field in fields:
                    fields[field].read_only = True
        return fields
