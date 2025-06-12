from rest_framework import generics
from .models import ClassroomEquipment, SchoolMaterialBase
from .serializers import ClassroomEquipmentSerializer, SchoolMaterialBaseSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ClassroomEquipmentListView(generics.ListAPIView):
    queryset = ClassroomEquipment.objects.select_related(
        "equipment",
    ).all()
    serializer_class = ClassroomEquipmentSerializer


class SchoolMaterialBaseListView(generics.ListAPIView):
    serializer_class = SchoolMaterialBaseSerializer

    def get_queryset(self):
        return SchoolMaterialBase.objects.select_related(
            "material",
        ).all()


class SchoolMaterialBaseUpdateView(generics.UpdateAPIView):
    queryset = SchoolMaterialBase.objects.all()
    serializer_class = SchoolMaterialBaseSerializer
    lookup_field = "pk"
