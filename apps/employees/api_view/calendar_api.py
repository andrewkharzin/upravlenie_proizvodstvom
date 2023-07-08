from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from apps.employees.models import EmplEvent

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        event_data = json.loads(request.body)
        # Извлечение данных из запроса и создание объекта CalendarEvent
        event = EmplEvent(
            title=event_data['title'],
            start=event_data['start'],
            end=event_data['end'],
            className=event_data['className'],
            allDay=event_data['allDay']
        )
        event.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def read_events(request):
    events = EmplEvent.objects.all()
    events_data = []
    for event in events:
        # Формирование данных для каждого события
        event_data = {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat(),
            'className': event.className,
            'allDay': event.allDay
        }
        events_data.append(event_data)
    return JsonResponse(events_data, safe=False)



@csrf_exempt
def update_event(request, event_id):
    if request.method == 'PUT':
        event = EmplEvent.objects.get(id=event_id)
        event_data = json.loads(request.body)
        # Обновление данных события
        event.title = event_data['title']
        event.start = event_data['start']
        event.end = event_data['end']
        event.className = event_data['className']
        event.allDay = event_data['allDay']
        event.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'DELETE':
        event = EmplEvent.objects.get(id=event_id)
        event.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
