# Generated by Django 3.2 on 2021-05-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_carpark_slot_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpark',
            name='ip_adress',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
