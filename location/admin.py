from django.contrib import admin
from .models import Region, District, School

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'school_number', 'school_type', 'district', 'region', 'director_full_name')
    search_fields = ('school_number', 'director_full_name', 'district__name', 'region__name')
    list_filter = ('school_type', 'region', 'district')