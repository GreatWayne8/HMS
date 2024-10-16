from django.shortcuts import render, get_object_or_404, redirect
from .models import Teleconsultation
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def start_teleconsultation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    teleconsultation, created = Teleconsultation.objects.get_or_create(appointment=appointment, patient=appointment.patient, doctor=appointment.doctor)
    return render(request, 'teleconsultation/start_consultation.html', {'teleconsultation': teleconsultation})

@login_required
def end_teleconsultation(request, consultation_id):
    teleconsultation = get_object_or_404(Teleconsultation, id=consultation_id)
    if request.method == "POST":
        teleconsultation.end_time = timezone.now()
        teleconsultation.call_summary = request.POST.get('call_summary', '')
        teleconsultation.status = 'completed'
        teleconsultation.save()
        return redirect('teleconsultation_list')
    return render(request, 'teleconsultation/end_consultation.html', {'teleconsultation': teleconsultation})

@login_required
def teleconsultation_list(request):
    consultations = Teleconsultation.objects.filter(patient=request.user) if request.user.is_patient else Teleconsultation.objects.filter(doctor=request.user)
    return render(request, 'teleconsultation/consultation_list.html', {'consultations': consultations})
