from django_cron import CronJobBase, Schedule
from ..models import PacketEvent, PacketType1
from loguru import logger as llogger
from tqdm import tqdm

class ReadUnreadPacketsCronJob(CronJobBase):
	RUN_EVERY_MINS = 0.25

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'supernova_app.ReadUnreadPacketsCronJob' # a unique code

	@llogger.catch
	def do(self):
		print("Running ReadUnreadPacketsCronJob...")
		
		while 1:
			# get all PacketEvent objects that aren't yet PacketType1 objects
			# and create PacketType1 objects from them
			
			packet_events = PacketEvent.objects.filter(packet_type_1__isnull=True)[:100]

			# TODO add a case where it re-calculates if the struct's string hash changed (i.e., different decode schema)

			if len(packet_events) == 0:
				#llogger.info(f"End of updates.")
				break # all done

			llogger.info(f"Read ({len(packet_events)}) PacketEvent objects that aren't yet PacketType1 objects")

			for packet_event in tqdm(packet_events):
				# Create a new PacketType1 object based on PacketEvent data
				packet_type_1 = PacketType1.construct_from_base64(
					packet_event.payload,
					request_uuid=packet_event,
					request_timestamp_utc=packet_event.request_timestamp_utc,
					request_helium_integration_details=packet_event.request_helium_integration_details,
				)

				# Associate the PacketType1 object with the PacketEvent
				packet_type_1.request_uuid = packet_event

				# Save the PacketType1 object
				packet_type_1.save()
