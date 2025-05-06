from rest_framework import serializers
from .models import MyGovTeacherLog

class MyGovTeacherLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGovTeacherLog
        fields = '__all__'
