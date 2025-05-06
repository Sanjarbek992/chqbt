from rest_framework import serializers
from .models import EmaktabStudent

class EmaktabStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmaktabStudent
        fields = "__all__"