from rest_framework import viewsets
from .models import Competition, CompetitionParticipant
from .serializers import CompetitionSerializer, CompetitionParticipantSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        user_profile = getattr(user, "userprofile", None)

        # Respublika — barcha
        if user.role == "superadmin":
            return queryset

        # Viloyat
        if user.role == "moderator" and user_profile and user_profile.oblast:
            return queryset.filter(organizer__oblastid=user_profile.oblast)

        # Tuman
        if user.role == "admin" and user_profile and user_profile.region:
            return queryset.filter(organizer__regionid=user_profile.region)

        # Maktab
        if user.role == "teacher" and user_profile and user_profile.school:
            return queryset.filter(organizer=user_profile.school)

        return queryset.none()


class CompetitionParticipantViewSet(viewsets.ModelViewSet):
    queryset = CompetitionParticipant.objects.all()
    serializer_class = CompetitionParticipantSerializer
