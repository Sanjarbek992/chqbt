from django.db import models
from .school_models import School


class Student(models.Model):
    pinfl = models.CharField(max_length=14, unique=True, verbose_name="PINFL", db_column="pinfl", db_index=True)
    full_name = models.CharField(max_length=255, verbose_name="F.I.SH.", db_column="full_name")
    birth_date = models.DateField(verbose_name="Tug`ilgan sana", db_column="birth_date")
    gender = models.CharField(max_length=10, verbose_name="Jinsi", db_column="gender")
    document_series = models.CharField(max_length=10, blank=True, verbose_name="Hujjat seriyasi",
                                       db_column="doc_series")
    document_number = models.CharField(max_length=20, blank=True, verbose_name="Hujjat raqami", db_column="doc_number")
    mfy_name = models.CharField(max_length=255, blank=True, verbose_name="MFY nomi", db_column="mfy_name")
    grade = models.CharField(max_length=20, verbose_name="Sinfi", db_column="grade", db_index=True)
    class_letter = models.CharField(max_length=20, verbose_name="Sinf harfi", db_column="class_letter")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name="students",
                               verbose_name="Maktab", db_column="school_id")
    school_year = models.CharField(max_length=20, verbose_name="o`quv yili", db_column="school_year")
    address = models.TextField(verbose_name="Yashash manzili", db_column="address", blank=True)
    oblast_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Viloyat ID", db_column="oblast_id")
    region_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tuman ID", db_column="region_id")
    school_grade_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Sinflar ID",
                                                  db_column="school_grade_id")
    org_school_grade_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Sinf (harf) ID",
                                                      db_column="org_school_grade_id")
    school_year_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="O‘quv yili ID",
                                                 db_column="school_year_id")
    mfy_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="MFY ID", db_column="mfy_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti", db_column="created_at")

    class Meta:
        verbose_name = "O`quvchi"
        verbose_name_plural = "O`quvchilar"
        db_table = "emaktab_students"
        indexes = [
            models.Index(fields=["grade"]),
            models.Index(fields=["pinfl"]),  # unikal qidiruv uchun
            models.Index(fields=["school"]),  # maktabga qarab filterlash
            models.Index(fields=["oblast_id"]),  # viloyat bo‘yicha tahlil
            models.Index(fields=["region_id"]),  # tuman bo‘yicha tahlil
            models.Index(fields=["school_year_id"]),  # o‘quv yili statistikasi
            models.Index(fields=["org_school_grade_id"]),  # sinf-harf uchun
            models.Index(fields=["mfy_id"]),  # mahalla bo‘yicha tahlil
        ]

    def __str__(self):
        return f"{self.full_name} ({self.school})"
