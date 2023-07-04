from django.urls import path
from .views import get_price_for_work, calendar_view
from .api_view import calendar_api
app_name = "employees"

urlpatterns = [
    path('get_price_for_work/', get_price_for_work, name='get_price_for_work'),
    # Маршруты событий
    path('calendar/', calendar_view, name='calendar'),
    path('events/', calendar_api.read_events, name='read_events'),
    path('events/create/', calendar_api.create_event, name='create_event'),
    path('events/update/<int:event_id>/', calendar_api.update_event, name='update_event'),
    path('events/delete/<int:event_id>/', calendar_api.delete_event, name='delete_event'),
]



