from rest_framework.serializers import ModelSerializer
from .models.school_models import School
from .models.student_models import Student
from .models.teacher_models import Teacher


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
