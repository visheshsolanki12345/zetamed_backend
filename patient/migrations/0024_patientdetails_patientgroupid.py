# Generated by Django 3.2.7 on 2022-03-13 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0023_auto_20220311_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdetails',
            name='patientGroupId',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]