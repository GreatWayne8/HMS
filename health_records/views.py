from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HealthRecord
from users.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView


@login_required
def patient_health_records(request):
    patient = request.user
    records = HealthRecord.objects.filter(patient=patient)
    return render(request, 'health_records/patient_records.html', {'records': records})

@login_required
def doctor_view_health_records(request, patient_id):
    if not request.user.is_doctor:
        return render(request, '403.html')  # Unauthorized if not a doctor
    patient = get_object_or_404(CustomUser, id=patient_id, is_patient=True)
    records = HealthRecord.objects.filter(patient=patient)

    if request.method == 'POST':
        # Update the health record (e.g., diagnosis, treatment)
        record_id = request.POST.get('record_id')
        health_record = HealthRecord.objects.get(id=record_id)
        health_record.diagnosis = request.POST.get('diagnosis')
        health_record.treatment_plan = request.POST.get('treatment_plan')
        health_record.lab_results = request.POST.get('lab_results')
        health_record.save()
        return redirect('doctor_view_health_records', patient_id=patient.id)

    return render(request, 'health_records/doctor_view_records.html', {
        'patient': patient, 
        'records': records
    })

class DoctorUpdateHealthRecordView(PermissionRequiredMixin, UpdateView):
    model = HealthRecord
    fields = ['diagnosis', 'treatment_plan', 'lab_results']
    permission_required = 'health_records.change_healthrecord'
    template_name = 'health_records/doctor_update_record.html'
    success_url = '/success/'  # Redirect to a success page or to the patient's records page

    def get_queryset(self):
        """Restrict the queryset to only allow doctors to edit records of their patients."""
        return HealthRecord.objects.filter(patient=self.request.user)
