from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, StudentViewSet, SchoolViewSet

router = DefaultRouter()
router.register(r"school", SchoolViewSet, basename="school")
router.register(r"teacher", TeacherViewSet, basename="teacher")
router.register(r"student", StudentViewSet, basename="student")
urlpatterns = [
    path("", include(router.urls)),
]
