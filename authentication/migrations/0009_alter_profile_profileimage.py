# Generated by Django 3.2.7 on 2022-03-09 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_profile_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileImage',
            field=models.ImageField(blank=True, null=True, upload_to='profile-images'),
        ),
    ]
