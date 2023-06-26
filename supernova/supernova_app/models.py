from django.db import models
import uuid
import cstruct
import base64
import datetime

class RawRequestLog(models.Model):
	request_uuid = models.UUIDField(primary_key=True)
	request_timestamp_utc = models.DateTimeField()
	request_helium_integration_details = models.CharField(max_length=255, null=True)
	request_text = models.CharField(max_length=8000)

	class Meta:
		db_table = 'supernova_raw_request_log'

class PacketEvent(models.Model):
	request_uuid = models.OneToOneField(RawRequestLog, primary_key=True, on_delete=models.CASCADE, db_column='request_uuid')
	request_timestamp_utc = models.DateTimeField()
	request_helium_integration_details = models.CharField(max_length=255, null=True)

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
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	# one-to-many relationship with PacketEvent (one packet can have many hotspots)
	request_uuid = models.ForeignKey(PacketEvent, on_delete=models.CASCADE, db_column='request_uuid')
	
	hotspot_num_within_packet = models.IntegerField(null=False) # starts at 0

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

		# TODO add a constrant to ensure hotspot_num_within_packet < PacketEvent.hotspot_count

class PacketType1(models.Model):
	request_uuid = models.OneToOneField(PacketEvent, primary_key=True, on_delete=models.CASCADE, db_column='request_uuid', related_name='packet_type_1')
	request_timestamp_utc = models.DateTimeField()
	request_helium_integration_details = models.CharField(max_length=255, null=True)

	packet_type = models.PositiveIntegerField()
	millis_since_boot = models.PositiveIntegerField()
	packet_seq_num = models.PositiveIntegerField()
	lora_dr_value = models.PositiveIntegerField()

	themistor_1_temperature_c = models.SmallIntegerField()
	themistor_2_temperature_c = models.SmallIntegerField()
	dht_temperature_c = models.SmallIntegerField()
	dht_humidity_pct = models.SmallIntegerField()
	bmp_pressure_pa = models.FloatField()
	bmp_temperature_c = models.FloatField()
	battery_voltage_mv = models.PositiveIntegerField()
	mcu_internal_temperature_c = models.SmallIntegerField()
	is_switch_rtf = models.BooleanField()

	gps_latitude_degrees = models.FloatField()
	gps_longitude_degrees = models.FloatField()
	gps_altitude_m = models.FloatField()
	gps_speed_m_per_s = models.FloatField()
	gps_course_degrees = models.FloatField()

	gps_satellite_count = models.PositiveIntegerField()
	gps_hdop_m = models.IntegerField()

	gps_fix_date_epoch_time_sec = models.PositiveIntegerField()
	gps_fix_date_age_ms = models.PositiveIntegerField()

	class Meta:
		db_table = 'supernova_packet_type_1'

	@classmethod
	def construct_from_base64(cls, base64_str: str, request_uuid: PacketEvent, request_timestamp_utc: datetime.datetime, request_helium_integration_details: str):
		"""
		Constructs a PacketType1 object from a hex string.
		"""

		class DataPacket1CStruct(cstruct.MemCStruct):
			__def__ = """
			
			struct {
				uint8_t packet_type; // always 1 for this struct
				uint32_t millis_since_boot;
				uint16_t packet_seq_num;
				uint8_t lora_dr_value;

				int8_t themistor_1_temperature_c;
				int8_t themistor_2_temperature_c;
				int8_t dht_temperature_c;
				int8_t dht_humidity_pct;
				float bmp_pressure_pa;
				float bmp_temperature_c;
				uint16_t battery_voltage_mv;
				int8_t mcu_internal_temperature_c;
				uint8_t is_switch_rtf; // TODO pack other bools in here, if we want

				// HERE is a good split if we ever wanted 2 different types of packets
				int32_t gps_latitude_degrees_x1e6;
				int32_t gps_longitude_degrees_x1e6;
				int32_t gps_altitude_cm;
				int32_t gps_speed_100ths_of_knot;
				int32_t gps_course_100ths_of_degree;
				uint16_t gps_satellite_count;
				int32_t gps_hdop_cm;
				uint32_t gps_fix_date_epoch_time_sec;
				uint32_t gps_fix_date_age_ms;
			};
			"""

		data = base64.b64decode(base64_str)
		packet = DataPacket1CStruct()
		packet.unpack(data)

		return cls(
			request_uuid=request_uuid,
			request_timestamp_utc=request_timestamp_utc,
			request_helium_integration_details=request_helium_integration_details,
			packet_type=packet.packet_type,
			millis_since_boot=packet.millis_since_boot,
			packet_seq_num=packet.packet_seq_num,
			lora_dr_value=packet.lora_dr_value,
			themistor_1_temperature_c=packet.themistor_1_temperature_c,
			themistor_2_temperature_c=packet.themistor_2_temperature_c,
			dht_temperature_c=packet.dht_temperature_c,
			dht_humidity_pct=packet.dht_humidity_pct,
			bmp_pressure_pa=packet.bmp_pressure_pa,
			bmp_temperature_c=packet.bmp_temperature_c,
			battery_voltage_mv=packet.battery_voltage_mv,
			mcu_internal_temperature_c=packet.mcu_internal_temperature_c,
			is_switch_rtf=packet.is_switch_rtf,
			gps_latitude_degrees=packet.gps_latitude_degrees_x1e6 / 1e6,
			gps_longitude_degrees=packet.gps_longitude_degrees_x1e6 / 1e6,
			gps_altitude_m=packet.gps_altitude_cm / 100,
			gps_speed_m_per_s=packet.gps_speed_100ths_of_knot / 100 * 0.514444444, # knots to m/s
			gps_course_degrees=packet.gps_course_100ths_of_degree / 100,
			gps_satellite_count=packet.gps_satellite_count,
			gps_hdop_m=packet.gps_hdop_cm / 100,
			gps_fix_date_epoch_time_sec=packet.gps_fix_date_epoch_time_sec,
			gps_fix_date_age_ms=packet.gps_fix_date_age_ms,
		)
	