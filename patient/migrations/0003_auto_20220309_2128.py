# Generated by Django 3.2.7 on 2022-03-09 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_isstaffcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdetails',
            name='proofId',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='patientdetails',
            name='whichProof',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
