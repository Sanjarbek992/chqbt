from django.db import models
from location.models import School

class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    pnfl = models.CharField(max_length=14, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    graduated_university = models.CharField(max_length=255)
    military_branch = models.CharField(max_length=255, blank=True, null=True)
    qualification_level = models.CharField(max_length=255)
    qualification_place = models.CharField(max_length=255)
    qualification_date = models.DateField()
    military_rank_date = models.DateField(blank=True, null=True)
    experience_years = models.IntegerField()
    is_vacant = models.BooleanField(default=False)
    def __str__(self): return f"{self.last_name} {self.first_name}"