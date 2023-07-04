from django.urls import path
from .views import get_price_for_work, calendar_view

app_name = "employees"

urlpatterns = [
    path('get_price_for_work/', get_price_for_work, name='get_price_for_work'),
    path('calendar/', calendar_view, name='calendar'),
]

