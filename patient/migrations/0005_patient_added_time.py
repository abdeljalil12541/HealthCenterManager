# Generated by Django 4.0.1 on 2024-04-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_patient_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='added_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
