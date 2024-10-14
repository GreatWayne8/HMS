from django.urls import path
from . import views
from .views import DoctorUpdateHealthRecordView, download_health_record

urlpatterns = [
    path('my-records/', views.patient_health_records, name='patient_health_records'),
    path('doctor-view/<int:patient_id>/', views.doctor_view_health_records, name='doctor_view_health_records'),
    path('health-records/edit/<int:pk>/', DoctorUpdateHealthRecordView.as_view(), name='doctor_update_health_record'),
    path('download-records/', download_health_record, name='download_health_record'),
]
