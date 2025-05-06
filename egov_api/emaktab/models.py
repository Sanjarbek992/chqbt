from django.db import models

class EmaktabStudent(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    school_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} ({self.grade})"
