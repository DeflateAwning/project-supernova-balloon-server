from django.db import models


class RawRequestLog(models.Model):
	request_uuid = models.UUIDField(primary_key=True)
	request_timestamp_utc = models.DateTimeField()
	request_text = models.CharField(max_length=8000)

	class Meta:
		db_table = 'supernova_raw_request_log'

class PacketEvent(models.Model):
	request_uuid = models.OneToOneField(RawRequestLog, primary_key=True, on_delete=models.CASCADE, db_column='request_uuid')
	request_timestamp_utc = models.DateTimeField()

	app_eui = models.CharField(max_length=16)
	dc_balance = models.IntegerField()
	dc_nonce = models.IntegerField()
	dev_eui = models.CharField(max_length=16)
	devaddr = models.CharField(max_length=8)
	downlink_url = models.URLField()
	fcnt = models.IntegerField()
	id = models.UUIDField()
	hotspot_count = models.IntegerField()
	metadata_adr_allowed = models.BooleanField()
	metadata_cf_list_enabled = models.BooleanField()
	metadata_multi_buy = models.IntegerField()
	metadata_organization_id = models.CharField(max_length=36)
	metadata_preferred_hotspots = models.JSONField()
	metadata_rx_delay = models.IntegerField()
	metadata_rx_delay_actual = models.IntegerField()
	metadata_rx_delay_state = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	payload = models.CharField(max_length=255)
	payload_size = models.IntegerField()
	port = models.IntegerField()
	raw_packet = models.CharField(max_length=255)
	replay = models.BooleanField()
	reported_at = models.BigIntegerField()
	type = models.CharField(max_length=255)
	uuid = models.UUIDField()

	class Meta:
		db_table = 'supernova_packet_event'
	
class PacketEventHotspot(models.Model):
	id = models.UUIDField(primary_key=True, auto_created=True)

	# one-to-many relationship with PacketEvent (one packet can have many hotspots)
	request_uuid = models.ForeignKey(PacketEvent, on_delete=models.CASCADE, db_column='request_uuid')
	
	hotspot_num_within_packet = models.IntegerField(null=False)

	channel = models.IntegerField()
	frequency = models.FloatField()
	hold_time = models.IntegerField()
	hotspot_id = models.CharField(max_length=255) # renamed from 'id'
	lat = models.FloatField()
	long = models.FloatField()
	name = models.CharField(max_length=255)
	reported_at = models.BigIntegerField()
	rssi = models.FloatField()
	snr = models.FloatField()
	spreading = models.CharField(max_length=255)
	status = models.CharField(max_length=255)

	class Meta:
		db_table = 'supernova_packet_event_hotspot'

		# set a unique key
		unique_together = (('request_uuid', 'hotspot_num_within_packet'),)
