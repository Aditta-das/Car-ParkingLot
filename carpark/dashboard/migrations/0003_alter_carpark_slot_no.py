# Generated by Django 3.2 on 2021-05-01 06:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_carpark_slot_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpark',
            name='slot_no',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(1)]),
        ),
    ]
