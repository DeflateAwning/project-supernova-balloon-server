from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import uuid
import os

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


@csrf_exempt
def api_v1_process_incoming_helium_packet(request):
	if request.method != 'POST':
		return JsonResponse({'message': 'Invalid request method', 'value': request.method}, status=405)
	
	if (content_type := request.headers.get('Content-Type')) != 'application/json':
		return JsonResponse({'message': 'Invalid content type', 'value': content_type}, status=415)
	
	if (secret_header := request.headers.get('X-Helium-Secret')) != os.environ.get('HELIUM_HEADER_SECRET'):
		return JsonResponse({'message': 'Invalid X-Helium-Secret header', 'value': secret_header}, status=403)

	data = json.loads(request.body)
	
	# Create RawRequestLog instance
	raw_request_log = RawRequestLog(
		request_uuid=uuid.uuid4(),
		request_timestamp_utc=datetime.utcnow(),
		request_text=request.body.decode('utf-8')
	)
	raw_request_log.save()
	
	# Create PacketEvent instance
	packet_event = PacketEvent(
		request_uuid=raw_request_log,
		request_timestamp_utc=datetime.utcnow(),
		app_eui=data['app_eui'],
		dc_balance=data['dc']['balance'],
		dc_nonce=data['dc']['nonce'],
		dev_eui=data['dev_eui'],
		devaddr=data['devaddr'],
		downlink_url=data['downlink_url'],
		fcnt=data['fcnt'],
		id=data['id'],
		hotspot_count=len(data['hotspots']),
		metadata_adr_allowed=data['metadata']['adr_allowed'],
		metadata_cf_list_enabled=data['metadata']['cf_list_enabled'],
		metadata_multi_buy=data['metadata']['multi_buy'],
		metadata_organization_id=data['metadata']['organization_id'],
		metadata_preferred_hotspots=data['metadata']['preferred_hotspots'],
		metadata_rx_delay=data['metadata']['rx_delay'],
		metadata_rx_delay_actual=data['metadata']['rx_delay_actual'],
		metadata_rx_delay_state=data['metadata']['rx_delay_state'],
		name=data['name'],
		payload=data['payload'],
		payload_size=data['payload_size'],
		port=data['port'],
		raw_packet=data['raw_packet'],
		replay=data['replay'],
		reported_at=data['reported_at'],
		type=data['type'],
		uuid=data['uuid']
	)
	packet_event.save()
	
	# Create PacketEventHotspot instances
	hotspots_data = data['hotspots']
	for hotspot_num_within_packet, hotspot_data in enumerate(hotspots_data):
		hotspot = PacketEventHotspot(
			request_uuid=packet_event,
			hotspot_num_within_packet=hotspot_num_within_packet,
			channel=hotspot_data['channel'],
			frequency=hotspot_data['frequency'],
			hold_time=hotspot_data['hold_time'],
			hotspot_id=hotspot_data['id'],
			lat=hotspot_data['lat'],
			long=hotspot_data['long'],
			name=hotspot_data['name'],
			reported_at=hotspot_data['reported_at'],
			rssi=hotspot_data['rssi'],
			snr=hotspot_data['snr'],
			spreading=hotspot_data['spreading'],
			status=hotspot_data['status']
		)
		hotspot.save()
	
	return JsonResponse({'message': 'Data saved successfully'})

