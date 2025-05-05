from rest_framework import serializers
from .models import Teacher
from location.serializers import SchoolSerializer

class TeacherListSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Teacher
        fields = [
            'id', 'pnfl', 'last_name', 'first_name', 'school', 'is_vacant'
        ]


class TeacherDetailSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), source='school', write_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'school', 'school_id', 'pnfl', 'last_name', 'first_name', 'middle_name',
            'birth_date', 'birth_place', 'specialty', 'graduated_university',
            'military_branch', 'qualification_level', 'qualification_place',
            'qualification_date', 'military_rank_date', 'experience_years', 'is_vacant'
        ]
