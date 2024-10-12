from django import forms
from .models import Patient, Doctor, Appointment, MedicalRecord
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):  
    email = forms.EmailField()  

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  

# Patient Form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'phone']

# Doctor Form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'specialization']

# Appointment Form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date']

# Medical Record Form
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'notes']
