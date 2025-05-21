from django.db import models
from .student_models import School


class Teacher(models.Model):
    pinfl = models.CharField(max_length=14, unique=True, verbose_name="PINFL", db_column="pinfl")
    first_name = models.CharField(max_length=55, verbose_name="Ismi", db_column="first_name")
    last_name = models.CharField(max_length=55, verbose_name="Familiya", db_column="last_name")
    middle_name = models.CharField(max_length=55, blank=True, verbose_name="Otasining ismi", db_column="middle_name")
    birth_date = models.DateField(verbose_name="Tug`ilgan sana", db_column="birth_date")
    gender = models.CharField(max_length=10, verbose_name="Jinsi", db_column="gender")
    document_series = models.CharField(max_length=10, blank=True, verbose_name="Hujjat seriyasi",
                                       db_column="doc_series")
    document_number = models.CharField(max_length=20, blank=True, verbose_name="Hujjat raqami", db_column="doc_number")
    region = models.CharField(max_length=100, blank=True, verbose_name="Tuman", db_column="region")
    oblast = models.CharField(max_length=100, blank=True, verbose_name="Viloyat", db_column="oblast")
    organisation_id = models.PositiveIntegerField(verbose_name="Maktab ID", db_column="organisation_id")
    organisation_name = models.CharField(max_length=255, verbose_name="Maktab nomi", db_column="organisation_name")
    position_name = models.CharField(max_length=255, verbose_name="Lavozimi", db_column="position_name")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers", verbose_name="Maktab", db_column="school_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti", db_column="created_at")

    class Meta:
        verbose_name = "CHQBT rahbari"
        verbose_name_plural = "CHQBT rahbarlari"
        db_table = "mygov_teachers"
        indexes = [
            models.Index(fields=["pinfl"]),  # teacher pinfl bo‘yicha qidiruv
            models.Index(fields=["school"]),  # maktab bo‘yicha bog‘lanish
            models.Index(fields=["organisation_id"]),  # tashqi school ID
            models.Index(fields=["region"]),  # string region uchun (kerak bo‘lsa)
            models.Index(fields=["oblast"]),  # string oblast uchun (kerak bo‘lsa)
        ]



