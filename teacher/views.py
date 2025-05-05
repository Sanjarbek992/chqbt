from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher
from .serializers import TeacherListSerializer, TeacherDetailSerializer
from .filters import TeacherFilter
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('school')
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TeacherFilter
    search_fields = ['pnfl', 'last_name', 'first_name', 'specialty']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherDetailSerializer
