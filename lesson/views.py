from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lesson, LessonSchedule, LessonMaterial
from .serializers import (
    LessonListSerializer,
    LessonDetailSerializer,
    LessonScheduleSerializer,
    LessonMaterialSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class LessonViewSet(viewsets.ModelViewSet):
    queryset = (
        Lesson.objects.select_related("school")
        .prefetch_related("schedule", "materials")
        .all()
    )
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # ]
    # filterset_fields = ["grade", "lesson_type", "school"]
    search_fields = ["subject", "topic"]
    ordering_fields = ["date", "subject"]
    ordering = ["-date"]

    def get_serializer_class(self):
        if self.action == "list":
            return LessonListSerializer
        return LessonDetailSerializer


class LessonScheduleViewSet(viewsets.ModelViewSet):
    queryset = LessonSchedule.objects.select_related("lesson").all()
    serializer_class = LessonScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role in ["admin", "superadmin"]
        )


class LessonMaterialViewSet(viewsets.ModelViewSet):
    queryset = LessonMaterial.objects.select_related("lesson")
    serializer_class = LessonMaterialSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(
        detail=False,
        methods=["post"],
        url_path="upload",
        permission_classes=[IsAdminOrSuperAdmin],
    )
    def upload_material(self, request):
        lesson_id = request.data.get("lesson_id")
        file = request.FILES.get("file")

        if not lesson_id or not file:
            return Response(
                {"detail": "lesson_id va file majburiy."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lesson = get_object_or_404(Lesson, id=lesson_id)
        material = LessonMaterial.objects.create(lesson=lesson, file=file)
        serializer = self.get_serializer(material)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
