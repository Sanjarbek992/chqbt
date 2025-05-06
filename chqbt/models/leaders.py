from django.db import models
from chqbt.models.schools import School

class Leader(models.Model):
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    pnfl = models.CharField(max_length=14, unique=True)
    degree = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    reserve_from = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    rank_date = models.DateField()
    qualification_date = models.DateField()
    experience_years = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.full_name