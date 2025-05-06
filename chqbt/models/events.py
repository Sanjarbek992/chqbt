from django.db import models
from chqbt.models.schools import School

class EventCategory(models.TextChoices):
    CEREMONY = 'ceremony', 'Tadbir'
    COMPETITION = 'competition', 'Musobaqa'
    VETERAN = 'veteran', 'Vatan tayanchi'

class Event(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=EventCategory.choices)
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.name
