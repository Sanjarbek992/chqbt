from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EmaktabStudent
from .serializers import EmaktabStudentSerializer
from .services import sync_students

class EmaktabStudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, school_id):
        sync_students(school_id)
        students = EmaktabStudent.objects.filter(school_id=school_id)
        serializer = EmaktabStudentSerializer(students, many=True)
        return Response(serializer.data)
