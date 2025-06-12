from django.db import models


class School(models.Model):
    ext_id = models.PositiveIntegerField(
        unique=True, verbose_name="Tashqi ID", db_column="external_id"
    )
    inn = models.CharField(
        max_length=20, unique=True, verbose_name="INN", db_column="inn"
    )
    name = models.CharField(
        max_length=200, verbose_name="Maktab nomi", db_column="name", db_index=True
    )
    short_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Qisqa nomi",
        db_column="short_name",
        db_index=True,
    )
    address = models.TextField(verbose_name="Manzil", db_column="address", blank=True)
    region_id = models.PositiveIntegerField(
        verbose_name="TumanID", db_column="region_id"
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tuman",
        db_column="region",
        db_index=True,
    )
    region_soato_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Tuman kodi",
        db_column="region_soato_code",
    )
    oblast_id = models.PositiveIntegerField(
        verbose_name="OblastID", db_column="oblast_id"
    )
    oblast = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Viloyat",
        db_column="oblast",
        db_index=True,
    )
    oblast_soato_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Viloyat kodi",
        db_column="oblast_soato_code",
    )
    director = models.CharField(
        max_length=255, blank=True, verbose_name="Direktor", db_column="director"
    )
    contact_info = models.CharField(
        max_length=255, blank=True, verbose_name="Tel raqami", db_column="contact_info"
    )
    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True,
        blank=True,
        verbose_name="Kenglik",
        db_column="latitude",
    )
    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True,
        blank=True,
        verbose_name="Uzunlik",
        db_column="longitude",
    )

    class Meta:
        verbose_name = "Maktab"
        verbose_name_plural = "Maktablar"
        db_table = "emaktab_schools"
        indexes = [
            models.Index(fields=["ext_id"]),  # tashqi ID asosida sinxronizatsiya
            models.Index(fields=["inn"]),  # INN orqali identifikatsiya
            models.Index(fields=["region_id"]),  # tuman bo‘yicha maktablar statistikasi
            models.Index(
                fields=["oblast_id"]
            ),  # viloyat bo‘yicha maktablar statistikasi
            models.Index(fields=["region_soato_code"]),  # SOATOga asoslangan analiz
            models.Index(fields=["oblast_soato_code"]),
            models.Index(fields=["oblast", "region", "name"]),
        ]

    def __str__(self):
        return self.name
