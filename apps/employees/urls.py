from django.urls import path
from .views import get_price_for_work, calendar_view, employee_list, employee_detail, rate_employee
from .api_view import calendar_api
from .utils.rate_func import increase_rating, decrease_rating

app_name = "employees"

urlpatterns = [
    path('get_price_for_work/', get_price_for_work, name='get_price_for_work'),
    # Маршруты событий
    path('calendar/', calendar_view, name='calendar'),
    path('events/', calendar_api.read_events, name='read_events'),
    path('events/create/', calendar_api.create_event, name='create_event'),


    path('employees/', employee_list, name="employee_list" ),
    path('employee/<int:employee_id>/', employee_detail, name='employee_detail'),
    path('employee/<int:employee_id>/increase-rating/', increase_rating, name='increase_rating'),
    path('employee/<int:employee_id>/decrease-rating/', decrease_rating, name='decrease_rating'),
    path('employee/<int:employee_id>/rate/', rate_employee, name='rate_employee'),
]



