# Generated by Django 4.2.2 on 2023-06-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supernova_app', '0004_alter_packettype1_request_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packettype1',
            name='gps_hdop_m',
            field=models.FloatField(),
        ),
    ]
