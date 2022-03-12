# Generated by Django 3.2.7 on 2022-03-11 06:36

from django.db import migrations, models
import patient.models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_alter_patientdetails_patientimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='patientImage',
            field=models.ImageField(blank=True, default='patient-images/avtar.png', null=True, upload_to=patient.models.user_directory_path_main),
        ),
    ]
