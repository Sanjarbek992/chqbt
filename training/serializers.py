from rest_framework import serializers
from .models import Training, ClassTraining


class TrainingSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Training
        fields = ["id", "title", "type", "image", "description"]


class ClassTrainingSerializer(serializers.ModelSerializer):
    training_title = serializers.CharField(source="training.title", read_only=True)
    training_type = serializers.CharField(
        source="training.get_type_display", read_only=True
    )

    class Meta:
        model = ClassTraining
        fields = [
            "id",
            "training",
            "training_title",
            "training_type",
            "school",
            "date",
            "notes",
        ]
