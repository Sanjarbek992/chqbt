from django.db import models
from django.contrib.auth import get_user_model
from chqbt.models.schools import School

User = get_user_model()


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    date_uploaded = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
