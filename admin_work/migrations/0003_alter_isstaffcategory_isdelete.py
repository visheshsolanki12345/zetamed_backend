# Generated by Django 3.2.7 on 2022-03-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_work', '0002_isstaffcategory_isdelete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isstaffcategory',
            name='isDelete',
            field=models.BooleanField(default=False),
        ),
    ]