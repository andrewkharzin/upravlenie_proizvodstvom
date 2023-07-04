from django.urls import path
from .views import login_view, logout_view, session_lock_view

urlpatterns = [
    # Other URL patterns
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('session-lock/', session_lock_view, name='session_lock'),
]

