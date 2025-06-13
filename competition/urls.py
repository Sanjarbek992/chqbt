from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet, CompetitionParticipantViewSet

router = DefaultRouter()
router.register(r"competitions", CompetitionViewSet)
router.register(r"competition-participants", CompetitionParticipantViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
