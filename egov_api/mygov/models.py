from django.db import models

class MyGovTeacherLog(models.Model):
    full_name = models.CharField(max_length=255)
    response_data = models.JSONField()
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
