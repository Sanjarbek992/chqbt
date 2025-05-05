from rest_framework import serializers
from .models import Region, District, School

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), write_only=True, source='region')

    class Meta:
        model = District
        fields = ['id', 'name', 'region', 'region_id']

class SchoolListSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    district = serializers.StringRelatedField()

    class Meta:
        model = School
        fields = ['id', 'school_number', 'school_type', 'director_full_name', 'region', 'district']

class SchoolDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), write_only=True, source='region')
    district_id = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), write_only=True, source='district')

    class Meta:
        model = School
        fields = [
            'id', 'school_number', 'school_type', 'director_full_name', 'geo_location',
            'region', 'region_id', 'district', 'district_id'
        ]
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'school_number', 'school_type', 'director_full_name']
