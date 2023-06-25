from django.db import migrations, models

# Note: Modified by ChatGPT to set existing null values for the new cols to "default_value_historical"

default_value_historical = 'Supernova1_Balloon'

def fill_null_values(apps, schema_editor):
	PacketEvent = apps.get_model('supernova_app', 'PacketEvent')
	RawRequestLog = apps.get_model('supernova_app', 'RawRequestLog')

	# Update the existing records for PacketEvent
	PacketEvent.objects.filter(request_helium_integration_details__isnull=True).update(request_helium_integration_details=default_value_historical)

	# Update the existing records for RawRequestLog
	RawRequestLog.objects.filter(request_helium_integration_details__isnull=True).update(request_helium_integration_details=default_value_historical)


class Migration(migrations.Migration):

	dependencies = [
		('supernova_app', '0001_initial'),
	]

	operations = [
		migrations.AddField(
			model_name='packetevent',
			name='request_helium_integration_details',
			field=models.CharField(max_length=255, null=True),
		),
		migrations.AddField(
			model_name='rawrequestlog',
			name='request_helium_integration_details',
			field=models.CharField(max_length=255, null=True),
		),
		migrations.RunPython(fill_null_values),
	]
