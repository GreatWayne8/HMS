from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .forms import PatientForm, DoctorForm, AppointmentForm, MedicalRecordForm
from django.contrib.auth.forms import AuthenticationForm  

def home(request):
    return render(request, 'home.html')

# View to add a Patient
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')  
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

# View to add a Doctor
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list') 
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})

# View to create an Appointment
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to appointment list
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})

# View to add a Medical Record
def add_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_record_list')  # Redirect to record list
    else:
        form = MedicalRecordForm()
    return render(request, 'add_medical_record.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.is_patient:
                user.save()
                Patient.objects.create(user=user)
            if user.is_doctor:
                user.save()
                Doctor.objects.create(user=user)
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})