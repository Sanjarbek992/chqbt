from django.db import models
from egov_api.models.school_models import School

# from egov_api.models.student_models import SchoolClass


class CompetitionLevel(models.TextChoices):
    SCHOOL = "school", "Maktab"
    REGION = "region", "Tuman"
    OBLAST = "oblast", "Viloyat"
    REPUBLIC = "republic", "Respublika"


class ParticipantType(models.TextChoices):
    CLASS = "class", "Sinf"
    SCHOOL = "school", "Maktab"
    MAHALLA = "mahalla", "Mahalla yoshlari"


class Competition(models.Model):
    title = models.CharField(max_length=255, verbose_name="Musobaqa nomi")
    level = models.CharField(max_length=20, choices=CompetitionLevel.choices)
    date = models.DateField()
    organizer = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tashkilotchi maktab",
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Musobaqa"
        verbose_name_plural = "Musobaqalar"

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"


class CompetitionParticipant(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="participants"
    )
    participant_type = models.CharField(max_length=20, choices=ParticipantType.choices)
    # school_class = models.ForeignKey(
    #     SchoolClass, null=True, blank=True, on_delete=models.SET_NULL
    # )
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    external_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Mahalla yoki tashqi nom"
    )

    class Meta:
        verbose_name = "Ishtirokchi"
        verbose_name_plural = "Ishtirokchilar"

    def __str__(self):
        return self.external_name or self.school
