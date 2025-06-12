from rest_framework import viewsets

from .models.school_models import School
from .models.student_models import Student
from .models.teacher_models import Teacher
from .serializers import SchoolSerializer, TeacherSerializer, StudentSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
