from django.urls import path
from .views import (
    ClassroomEquipmentListView,
    SchoolMaterialBaseListView,
    SchoolMaterialBaseUpdateView
)

urlpatterns = [
    path('classroom-equipment/', ClassroomEquipmentListView.as_view()),
    path('omb/school/', SchoolMaterialBaseListView.as_view()),
    path('omb/school/<int:pk>/update/', SchoolMaterialBaseUpdateView.as_view()),
]
