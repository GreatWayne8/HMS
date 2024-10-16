from django import forms
from .models import Patient, Doctor
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_image']


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email'] 