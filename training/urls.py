from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingViewSet, ClassTrainingViewSet

router = DefaultRouter()
router.register(r"trainings", TrainingViewSet)
router.register(r"class-trainings", ClassTrainingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
