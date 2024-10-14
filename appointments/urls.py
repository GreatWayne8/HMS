from django.urls import path
from .views import schedule_appointment, view_appointments, view_patients  # Ensure view_appointments is defined

urlpatterns = [
    path('schedule/', schedule_appointment, name='schedule_appointment'),
    path('view/', view_appointments, name='view_appointments'),
    path('patients/', view_patients, name='view_patients'),
]
