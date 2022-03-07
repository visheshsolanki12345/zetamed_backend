# Generated by Django 3.2.7 on 2022-03-06 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('age', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=500, null=True)),
                ('mobileNo', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('city', models.CharField(blank=True, max_length=400, null=True)),
                ('state', models.CharField(blank=True, max_length=400, null=True)),
                ('country', models.CharField(blank=True, max_length=400, null=True)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
                ('problem', models.CharField(blank=True, max_length=500, null=True)),
                ('problemDescription', models.TextField(blank=True, null=True)),
                ('patientImage', models.ImageField(blank=True, null=True, upload_to='patient-images')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]