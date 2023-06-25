from django_cron import CronJobBase, Schedule
from ..models import PacketEvent

class ReadUnreadPacketsCronJob(CronJobBase):
	RUN_EVERY_MINS = 1 # every 1 minute

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'supernova_app.ReadUnreadPacketsCronJob'    # a unique code

	def do(self):
		print("Running ReadUnreadPacketsCronJob...")
		...

