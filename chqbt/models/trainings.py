from django.db import models
from chqbt.models.schools import School

class LessonType(models.TextChoices):
    THEORY = 'theory', 'Nazariy'
    PRACTICAL = 'practical', 'Amaliy'
    DEMO = 'demo', 'Ko‘rgazmali'

class Lesson(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    date = models.DateField()
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices)

    def __str__(self):
        return f"{self.subject} - {self.date}"

