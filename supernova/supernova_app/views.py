from django.shortcuts import render
from .models import RawRequestLog, PacketEventHotspot, PacketEvent

def index(request):
	raw_request_log_count = RawRequestLog.objects.count()
	packet_event_hotspot_count = PacketEventHotspot.objects.count()
	packet_event_count = PacketEvent.objects.count()

	app_name = 'Supernova UI'
	
	return render(
		request, 'index.html',
		context={
			'app_name': app_name,
			'raw_request_log_count': raw_request_log_count,
			'packet_event_hotspot_count': packet_event_hotspot_count,
			'packet_event_count': packet_event_count,
		}
	)
