# location/filters.py
import django_filters
from .models import School

class SchoolFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='region__id')
    district = django_filters.NumberFilter(field_name='district__id')
    school_type = django_filters.ChoiceFilter(field_name='school_type', choices=School._meta.get_field('school_type').choices)

    class Meta:
        model = School
        fields = ['region', 'district', 'school_type']
