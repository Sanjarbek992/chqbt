from rest_framework import serializers
from .models import Lesson, LessonSchedule, LessonMaterial


class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = ["id", "file", "uploaded_at"]


class LessonScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSchedule
        fields = ["id", "weekday", "time"]


class LessonListSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ["id", "subject", "topic", "grade", "lesson_type", "school", "date"]


class LessonDetailSerializer(serializers.ModelSerializer):
    schedule = LessonScheduleSerializer(many=True, read_only=True)
    materials = LessonMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "subject",
            "topic",
            "grade",
            "lesson_type",
            "date",
            "schedule",
            "materials",
        ]
