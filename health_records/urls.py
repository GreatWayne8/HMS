from django.urls import path
from . import views

urlpatterns = [
    path('my-records/', views.patient_health_records, name='patient_health_records'),
    path('doctor-view/<int:patient_id>/', views.doctor_view_health_records, name='doctor_view_health_records'),
]
