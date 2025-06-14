# Generated by Django 5.2 on 2025-05-26 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("egov_api", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="department",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="oblast",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Viloyat"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="organization_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Tashkilot nomi"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="passport_number",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="Passport raqami"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="position_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Lavozimi"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="region",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Tuman"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="school",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_profiles",
                to="egov_api.school",
                verbose_name="Maktab",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="passport_series",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="Passport seriyasi"
            ),
        ),
    ]
