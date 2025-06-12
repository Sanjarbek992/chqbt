from django.db import models
from django.contrib.auth import get_user_model
from chqbt.models.schools import School

User = get_user_model()


class Task(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "Yangi"),
            ("in_progress", "Jarayonda"),
            ("completed", "Bajarilgan"),
            ("delayed", "Kechikkan"),
        ],
        default="new",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    assigned_to = models.ManyToManyField(User, related_name="assigned_tasks")

    def __str__(self):
        return self.title
