# Generated by Django 3.2.7 on 2022-03-15 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0028_auto_20220315_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='isstaffcategorybyuser',
            name='isStaff',
        ),
        migrations.RemoveField(
            model_name='isstaffcategorybyuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='IsStaffCategory',
        ),
        migrations.DeleteModel(
            name='IsStaffCategoryByUser',
        ),
    ]