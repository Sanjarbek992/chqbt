from django.db import models
from egov_api.models.school_models import School


class MaterialBase(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="OMB mezoni")

    class Meta:
        verbose_name = "O`quv moddiy baza"
        verbose_name_plural = "O`quv moddiy baza"
        db_table = "material_base"

    def __str__(self):
        return self.name


class SchoolMaterialBase(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="material_base",
        verbose_name="Maktab",
        db_index=True,
    )
    material = models.ForeignKey(
        MaterialBase,
        on_delete=models.CASCADE,
        related_name="school_material_base",
        verbose_name="Baza",
        db_index=True,
    )
    is_available = models.BooleanField(null=True, verbose_name="Mavjudligi")

    class Meta:
        verbose_name = "Maktab o`quv moddiy bazasi"
        verbose_name_plural = "Maktab o`quv moddiy bazasi"
        unique_together = (("school", "material"),)
        db_table = "school_material_base"

    def __str__(self):
        return f"{self.school.name} - {self.material.name}: {'Bor' if self.is_available else 'Yo`q'}"


class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Jihoz nomi")
    standard_quantity = models.PositiveIntegerField(verbose_name="Shtat bo‘yicha soni")

    def __str__(self):
        return f"{self.name} - {self.standard_quantity} dona"

    class Meta:
        verbose_name = "Jihoz nomi"
        verbose_name_plural = "Jihozlar"
        db_table = "equipments"
        ordering = ["name"]


class ClassroomEquipment(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school",
        verbose_name="Maktab",
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name="Maktab jihozlari",
        related_name="equipment",
    )
    actual_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Amalda mavjud"
    )

    class Meta:
        verbose_name = "Jihoz holati"
        verbose_name_plural = "Jihoz holatlari"
        unique_together = ("school", "equipment")
        db_table = "classroom_equipments"

    def __str__(self):
        return (
            f"{self.school.name} - {self.equipment.name}: {self.actual_quantity} dona"
        )

    def percent_equipped(self):
        """Jihozlanish foizini hisoblaydi"""
        if self.equipment.standard_quantity == 0:
            return 0
        return round((self.actual_quantity / self.equipment.standard_quantity) * 100, 2)
