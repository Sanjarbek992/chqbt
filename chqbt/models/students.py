from django.db import models
from chqbt.models.schools import School


class Gender(models.TextChoices):
    MALE = "male", "O‘g‘il bola"
    FEMALE = "female", "Qiz bola"


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, db_index=True)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    grade = models.IntegerField(
        choices=[(10, "10-sinf"), (11, "11-sinf")], db_index=True
    )
    gender = models.CharField(max_length=6, choices=Gender.choices)
    grade_score = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    military_service = models.BooleanField(default=False)
    university = models.CharField(max_length=255, blank=True, null=True)
    pinfl = models.CharField(max_length=14, unique=True, db_index=True)

    def __str__(self):
        return self.full_name
