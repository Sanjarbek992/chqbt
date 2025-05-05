import django_filters
from .models import Teacher

class TeacherFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(field_name='school_id')
    is_vacant = django_filters.BooleanFilter()

    class Meta:
        model = Teacher
        fields = ['school', 'is_vacant']
