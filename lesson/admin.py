from django.contrib import admin
from .models import Lesson, LessonSchedule, LessonMaterial

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'topic', 'grade', 'lesson_type', 'school', 'date')
    list_filter = ('lesson_type', 'grade', 'school')
    search_fields = ('subject', 'topic')
    ordering = ('-date',)

@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'weekday', 'time')
    list_filter = ('weekday',)
    ordering = ('lesson', 'weekday')

@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
