from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Region, District, School
from .serializers import (
    RegionSerializer,
    DistrictSerializer,
    SchoolListSerializer,
    SchoolDetailSerializer
)
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'], url_path='school-stats')
    def school_statistics(self, request, pk=None):
        region = self.get_object()
        stats = (
            School.objects
            .filter(region=region)
            .values('school_type')
            .annotate(count=Count('id'))
        )
        total = School.objects.filter(region=region).count()
        return Response({
            "region": region.name,
            "total_schools": total,
            "by_type": {i['school_type']: i['count'] for i in stats}
        })

class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'region__name']

    def get_queryset(self):
        region_id = self.request.query_params.get('region_id')
        if region_id:
            return District.objects.filter(region_id=region_id)
        return District.objects.all()

    @action(detail=True, methods=['get'], url_path='school-stats')
    def school_statistics(self, request, pk=None):
        district = self.get_object()
        stats = (
            School.objects
            .filter(district=district)
            .values('school_type')
            .annotate(count=Count('id'))
        )
        total = School.objects.filter(district=district).count()
        return Response({
            "district": district.name,
            "total_schools": total,
            "by_type": {i['school_type']: i['count'] for i in stats}
        })

class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['school_number', 'director_full_name', 'district__name', 'region__name']

    def get_queryset(self):
        district_id = self.request.query_params.get('district_id')
        if district_id:
            return School.objects.filter(district_id=district_id)
        return School.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SchoolListSerializer
        return SchoolDetailSerializer
