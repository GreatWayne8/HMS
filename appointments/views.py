from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Appointment
from users.models import Patient, CustomUser
from django.utils import timezone
from datetime import datetime

@login_required
def schedule_appointment(request):
    try:
        patient = request.user.patient  
    except Patient.DoesNotExist:
        return render(request, 'appointments/error.html', {'error_message': 'You are not registered as a patient.'})

    doctors = CustomUser.objects.filter(is_doctor=True)

    if request.method == 'POST':
        doctor = request.POST.get('doctor')  
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        print(f'Doctor ID: {doctor}')  

        if appointment_date and appointment_time and doctor:
            appointment_datetime_str = f"{appointment_date} {appointment_time}"
            try:
                # Convert the string to a datetime object
                appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M')
                
                # Make it timezone-aware
                appointment_datetime = timezone.make_aware(appointment_datetime)

                # Create the Appointment instance
                appointment = Appointment(
                    patient=patient,
                    doctor_id=doctor,  
                    appointment_date=appointment_datetime,  # Now passing a timezone-aware datetime object
                    reason=reason
                )
                appointment.clean()
                appointment.save()

                return redirect('appointment_success')

            except ValueError:
                return render(request, 'appointments/schedule_appointment.html', {
                    'doctors': doctors,  # Pass doctors back to the template
                    'error': 'Invalid date/time format. Please use the correct format.'
                })
            except ValidationError as e:
                return render(request, 'appointments/schedule_appointment.html', {
                    'doctors': doctors,  
                    'error': e.messages
                })

    return render(request, 'appointments/schedule_appointment.html', {'doctors': doctors})


@login_required
def view_appointments(request):
    try:
        patient = request.user.patient 
    except Patient.DoesNotExist:
        return render(request, 'appointments/error.html', {'error_message': 'You are not registered as a patient.'})

    # If the patient exists, filter appointments by the patient
    appointments = Appointment.objects.filter(patient=patient)  
    return render(request, 'appointments/view_appointments.html', {'appointments': appointments})

@login_required
def view_patients(request):
    patients = Patient.objects.all()  
    return render(request, 'appointments/view_patients.html', {'patients': patients})
