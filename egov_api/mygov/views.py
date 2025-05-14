
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
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


from rest_framework import status

class FakeMygovAPIView(APIView):
    def get(self, request):
        pinfl = request.query_params.get("pinfl")

        if not pinfl or len(pinfl) != 14:
            return Response({"error": "PINFL 14 xonali bo‘lishi kerak"}, status=400)

        # soxta natija
        data = {
            "success": True,
            "date": "14.05.2025",
            "resultCount": 1,
            "result": {
                "id": 123456,
                "fullName": "SOXTA O‘QUVCHI ISMI",
                "dateOfBirth": "2009-09-09",
                "pinfl": pinfl,
                "genderName": "Erkak",
                "oblastName": "Toshkent viloyati",
                "regionName": "Bo‘ka tumani",
                "organizationName": "Xalq ta'limi maktabi №42",
                "schoolGradeName": "10-sinf",
                "orgschoolGradeName": "10-A",
                "adress": "Bo‘ka ko‘chasi, 42-uy"
            },
            "errorMessage": None
        }

        return Response(data, status=status.HTTP_200_OK)