# Generated by Django 4.0.1 on 2024-04-26 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_alter_patient_address_alter_patient_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='visit_date',
            field=models.DateField(default=datetime.date(2024, 4, 26), null=True),
        ),
    ]
