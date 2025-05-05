from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 'first_name', 'pnfl', 'school', 'specialty', 'qualification_level', 'is_vacant'
    )
    list_filter = ('school', 'is_vacant', 'qualification_level')
    search_fields = ('pnfl', 'last_name', 'first_name', 'specialty')
    ordering = ('last_name', 'first_name')
