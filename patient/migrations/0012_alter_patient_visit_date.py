# Generated by Django 4.0.1 on 2024-04-26 21:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_alter_patient_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='visit_date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
