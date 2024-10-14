from django.db import models
from users.models import CustomUser
from appointments.models import Appointment
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
import csv

class HealthRecord(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="health_records")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    lab_results = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Record for {self.patient.get_full_name()} on {self.date_created}"

@login_required
def download_health_record(request):
    patient = request.user
    records = HealthRecord.objects.filter(patient=patient)

    # Render the health records to HTML
    html_string = render_to_string('health_records/download_health_record.html', {'records': records})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_record.pdf"'
    
    # Create the PDF
    HTML(string=html_string).write_pdf(response)
    return response

@login_required
def download_health_record_csv(request):
    patient = request.user
    records = HealthRecord.objects.filter(patient=patient)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="health_record.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Diagnosis', 'Treatment Plan', 'Lab Results'])  # CSV header

    for record in records:
        writer.writerow([record.date_created, record.diagnosis, record.treatment_plan, record.lab_results])

    return response