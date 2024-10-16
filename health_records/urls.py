from django.urls import path
from . import views
from .views import DoctorUpdateMedicalRecordView, download_health_record_csv, download_health_record

urlpatterns = [
    path('my-records/', views.patient_health_records, name='patient_health_records'),
    path('doctor-view/<int:patient_id>/', views.doctor_view_health_records, name='doctor_view_health_records'),
    path('health-records/edit/<int:pk>/', DoctorUpdateMedicalRecordView.as_view(), name='doctor_update_health_record'),
    path('download-records/<int:record_id>/', download_health_record, name='download_health_record'),  # Updated path
    path('download-records/csv/<int:record_id>/', download_health_record_csv, name='download_health_record_csv'),
]
