from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .forms import PatientForm, DoctorForm, MedicalRecordForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Doctor  
from .models import MedicalRecord  # Import your MedicalRecord model
from .forms import  ProfileUpdateForm,CustomUserUpdateForm



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

# Dashboard views
@login_required
def patient_dashboard(request):
    return render(request, 'patients/dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctors/dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if request.POST.get('user_type') == 'patient':
            patient_form = PatientForm(request.POST)
            if user_form.is_valid() and patient_form.is_valid():
                user = user_form.save(commit=False)
                user.is_patient = True
                user.save()
                patient = patient_form.save(commit=False)
                patient.user = user
                patient.save()
                return redirect('login')
        elif request.POST.get('user_type') == 'doctor':
            doctor_form = DoctorForm(request.POST)
            if user_form.is_valid() and doctor_form.is_valid():
                user = user_form.save(commit=False)
                user.is_doctor = True
                user.save()
                doctor = doctor_form.save(commit=False)
                doctor.user = user
                doctor.save()
                return redirect('login')
    else:
        user_form = UserRegistrationForm()
        patient_form = PatientForm()
        doctor_form = DoctorForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'patient_form': patient_form,
        'doctor_form': doctor_form,
    })



@login_required  
def view_medical_records(request):

    medical_records = MedicalRecord.objects.filter(patient=request.user.patient)

    return render(request, 'patients/medical_records.html', {'medical_records': medical_records})



@login_required
def update_profile(request):
    user = request.user
    patient = user.patient

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)  
        patient_form = ProfileUpdateForm(request.POST, request.FILES, instance=patient) 

        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            return redirect('patient_dashboard')
    else:
        user_form = CustomUserUpdateForm(instance=user)
        patient_form = ProfileUpdateForm(instance=patient)

    return render(request, 'patients/update_profile.html', {
        'patient_form': patient_form,
        'user_form': user_form,
    })


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')  
            elif user.is_doctor:
                return redirect('doctor_dashboard') 
            elif user.is_superuser:  
                return redirect('admin_dashboard')  
            else:
                return redirect('home')  
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
