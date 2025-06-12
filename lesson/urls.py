from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, LessonScheduleViewSet, LessonMaterialViewSet

router = DefaultRouter()
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"schedules", LessonScheduleViewSet, basename="schedule")
router.register(r"materials", LessonMaterialViewSet, basename="material")

urlpatterns = [
    path("", include(router.urls)),
]
