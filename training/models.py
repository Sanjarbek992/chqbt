from django.db import models
from egov_api.models.school_models import School

# from egov_api.models.student_models import SchoolClass


class TrainingType(models.TextChoices):
    THEORETICAL = "theoretical", "Nazariy"
    PRACTICAL = "practical", "Amaliy"


def training_image_upload_path(instance, filename):
    return f"trainings/{instance.title}_{filename}"


class Training(models.Model):
    title = models.CharField(max_length=255, verbose_name="Mashg‘ulot nomi")
    type = models.CharField(
        max_length=20, choices=TrainingType.choices, verbose_name="Mashg‘ulot turi"
    )
    image = models.ImageField(
        upload_to=training_image_upload_path, blank=True, null=True, verbose_name="Rasm"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Mashg‘ulot"
        verbose_name_plural = "Mashg‘ulotlar"

    def __str__(self):
        return f"{self.get_type_display()} — {self.title}"


class ClassTraining(models.Model):
    training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name="sessions"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="trainings"
    )
    # school_class = models.ForeignKey(
    #     SchoolClass, on_delete=models.CASCADE, related_name="trainings"
    # )
    date = models.DateField(verbose_name="Mashg‘ulot o‘tkazilgan sana")
    notes = models.TextField(blank=True, null=True, verbose_name="Qo‘shimcha izoh")

    class Meta:
        verbose_name = "Sinf mashg‘uloti"
        verbose_name_plural = "Sinf mashg‘ulotlari"

    def __str__(self):
        return f"{self.training} ({self.date})"
