from django.urls import path
from .views import material_info

urlpatterns = [
    # Other URL patterns
    path('material-info/', material_info, name='material_info'),
]
