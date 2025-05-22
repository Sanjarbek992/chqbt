from rest_framework import generics
from .models import ClassroomEquipment, SchoolMaterialBase
from .serializers import ClassroomEquipmentSerializer, SchoolMaterialBaseSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ClassroomEquipmentListView(generics.ListAPIView):
    queryset = ClassroomEquipment.objects.select_related('equipment', 'school').all()
    serializer_class = ClassroomEquipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['school']


class SchoolMaterialBaseListView(generics.ListAPIView):
    serializer_class = SchoolMaterialBaseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['school']
    def get_queryset(self):
       return SchoolMaterialBase.objects.select_related('material','school').all()

class SchoolMaterialBaseUpdateView(generics.UpdateAPIView):
    queryset = SchoolMaterialBase.objects.all()
    serializer_class = SchoolMaterialBaseSerializer
    lookup_field = 'pk'