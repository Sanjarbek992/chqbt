from rest_framework import serializers
from .models import Competition, CompetitionParticipant


class CompetitionParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionParticipant
        fields = ["id", "participant_type", "school", "external_name"]


class CompetitionSerializer(serializers.ModelSerializer):
    participants = CompetitionParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = [
            "id",
            "title",
            "level",
            "date",
            "organizer",
            "description",
            "participants",
        ]
