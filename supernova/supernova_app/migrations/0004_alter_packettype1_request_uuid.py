# Generated by Django 4.2.2 on 2023-06-25 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supernova_app', '0003_packettype1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packettype1',
            name='request_uuid',
            field=models.OneToOneField(db_column='request_uuid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='packet_type_1', serialize=False, to='supernova_app.packetevent'),
        ),
    ]
