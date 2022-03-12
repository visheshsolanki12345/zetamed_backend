# Generated by Django 3.2.7 on 2022-03-11 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_auto_20220311_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientbyuser',
            name='patientGroup',
        ),
        migrations.AddField(
            model_name='patientbyuser',
            name='patientGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.patientgroupbyuser'),
        ),
    ]