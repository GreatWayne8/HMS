from django.urls import path
from .views import (
    home, 
    register, 
    login_user, 
    add_patient, 
    add_doctor, 
    add_medical_record,
    patient_dashboard, 
    doctor_dashboard, 
    update_profile,  #
    admin_dashboard,
    view_medical_records,
)

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('add_patient/', add_patient, name='add_patient'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('view_medical_records/', view_medical_records, name='view_medical_records'),
    path('add_medical_record/', add_medical_record, name='add_medical_record'),
    path('patient_dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),   
    path('update_profile/', update_profile, name='update_profile'),  
]
