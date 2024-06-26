# Generated by Django 4.0.1 on 2024-04-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='detail',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='medecine_detail',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='next_visit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='note',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
