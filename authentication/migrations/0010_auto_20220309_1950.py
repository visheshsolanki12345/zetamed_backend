# Generated by Django 3.2.7 on 2022-03-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_profile_profileimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpverify',
            name='isBlockNumber',
        ),
        migrations.AddField(
            model_name='otpverify',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]