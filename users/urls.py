from django.urls import path
from .views import (
    home, 
 
    register, 
    login_user, 
    add_patient, 
    add_doctor, 
    create_appointment, 
    add_medical_record
)

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('add_patient/', add_patient, name='add_patient'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('create_appointment/', create_appointment, name='create_appointment'),
    path('add_medical_record/', add_medical_record, name='add_medical_record'),
    # Add other paths as necessary
]
