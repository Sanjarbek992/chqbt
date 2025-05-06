
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from teacher.models import Teacher
from .services import sync_teacher_data
from .models import MyGovTeacherLog
from .serializers import MyGovTeacherLogSerializer

class MyGovSyncAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        credentials = request.data.get("credentials")
        query = request.data.get("query")
        data = sync_teacher_data(
            username=credentials["username"],
            password=credentials["password"],
            key=credentials["consumer_key"],
            secret=credentials["consumer_secret"],
            query=query
        )
        log = MyGovTeacherLog.objects.create(full_name=data["full_name"], response_data=data)
        return Response(MyGovTeacherLogSerializer(log).data)
