from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): return self.name


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self): return f"{self.region.name} - {self.name}"


class SchoolType(models.TextChoices):
    GENERAL = 'general', 'Umumta`lim'
    SPECIALIZED = 'specialized', 'Ixtisoslashtirilgan'
    JASORAT = 'jasorat', 'Jasorat maktabi'


class School(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    school_number = models.PositiveIntegerField()
    school_type = models.CharField(max_length=20, choices=SchoolType.choices)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.school_number} - {self.get_school_type_display()}"