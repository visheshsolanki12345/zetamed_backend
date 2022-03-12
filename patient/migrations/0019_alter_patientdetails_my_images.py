# Generated by Django 3.2.7 on 2022-03-11 11:36

from django.db import migrations, models
import patient.models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_patientdetails_my_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='my_images',
            field=models.ImageField(default='patient-images/avtar.png', upload_to=patient.models.user_directory_path_main),
        ),
    ]
