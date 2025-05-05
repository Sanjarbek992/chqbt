from django.db import models
from location.models import School
from django.utils.translation import gettext_lazy as _

class LessonType(models.TextChoices):
    THEORY = 'theory', _('Nazariy')
    PRACTICAL = 'practical', _('Amaliy')
    DEMO = 'demo', _('Ko‘rgazmali')

class Lesson(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='lessons', db_index=True)
    subject = models.CharField(max_length=255, verbose_name=_("Fan"))
    topic = models.CharField(max_length=255, verbose_name=_("Mavzu"))
    date = models.DateField(verbose_name=_("Sana"), db_index=True)
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices, verbose_name=_("Mashg‘ulot turi"), db_index=True)
    grade = models.IntegerField(choices=[(10, '10-sinf'), (11, '11-sinf')], verbose_name=_("Sinf"), db_index=True)

    def __str__(self):
        return f"{self.subject} ({self.get_lesson_type_display()}) - {self.topic}"

    class Meta:
        verbose_name = _("Dars")
        verbose_name_plural = _("Darslar")
        indexes = [
            models.Index(fields=['school', 'grade']),
            models.Index(fields=['school', 'date']),
            models.Index(fields=['lesson_type', 'grade']),
        ]

class LessonSchedule(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='schedule')
    weekday = models.CharField(max_length=20, verbose_name=_("Hafta kuni"))
    time = models.TimeField(verbose_name=_("Vaqti"))

    def __str__(self):
        return f"{self.lesson.subject} - {self.weekday} ({self.time})"

    class Meta:
        verbose_name = _("Dars jadvali")
        verbose_name_plural = _("Dars jadvallari")

class LessonMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials', db_index=True)
    file = models.FileField(upload_to='lesson_materials/', verbose_name=_("Fayl"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yuklangan vaqti"),db_index=True)

    def __str__(self):
        return f"📎 {self.lesson.subject} — {self.lesson.topic}"

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Dars materiallari")
