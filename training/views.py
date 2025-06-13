from rest_framework import viewsets
from .models import Training, ClassTraining
from .serializers import TrainingSerializer, ClassTrainingSerializer
from users.models import Role
from rest_framework.permissions import IsAuthenticated


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer


class ClassTrainingViewSet(viewsets.ModelViewSet):
    queryset = ClassTraining.objects.select_related(
        "training", "school", "school_class"
    )
    serializer_class = ClassTrainingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = getattr(user, "userprofile", None)
        queryset = super().get_queryset()

        # Parametrlar orqali maxsus filtr (masalan, tuman admini maktabni ko'rmoqchi bo'lsa)
        school_id = self.request.query_params.get("school_id")
        if school_id:
            return queryset.filter(school_id=school_id)

        # Foydalanuvchi roliga qarab filtr
        if user.role == Role.TEACHER:
            if user_profile and user_profile.school:
                return queryset.filter(school=user_profile.school)

        elif user.role == Role.ADMIN:  # tuman admini
            if user_profile and user_profile.region:
                return queryset.filter(school__regionid=user_profile.region)

        elif user.role == Role.MODERATOR:  # viloyat
            if user_profile and user_profile.oblast:
                return queryset.filter(school__oblastid=user_profile.oblast)

        elif user.role == Role.SUPERADMIN:
            return queryset  # barcha ma’lumotlar

        return queryset.none()
