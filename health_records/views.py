from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import MedicalRecord
from users.models import CustomUser
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView
from django.http import HttpResponse
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from .forms import MedicalRecordForm
from .models import MedicalRecord
from reportlab.platypus import Image


@login_required
def patient_health_records(request):
    patient = request.user
    records = MedicalRecord.objects.filter(patient=patient)
    return render(request, 'health_records/patient_records.html', {'records': records})

@login_required
def doctor_view_health_records(request, patient_id):
    if not request.user.is_doctor:
        raise PermissionDenied  # Use PermissionDenied for unauthorized access

    patient = get_object_or_404(CustomUser, id=patient_id, is_patient=True)
    records = MedicalRecord.objects.filter(patient=patient)

    if request.method == 'POST':
        # Update the health record (e.g., diagnosis, treatment)
        record_id = request.POST.get('record_id')
        health_record = get_object_or_404(MedicalRecord, id=record_id, patient=patient)
        health_record.diagnosis = request.POST.get('diagnosis')
        health_record.treatment_plan = request.POST.get('treatment_plan')
        health_record.lab_results = request.POST.get('lab_results')
        health_record.save()
        return redirect('doctor_view_health_records', patient_id=patient.id)

    return render(request, 'health_records/doctor_view_records.html', {
        'patient': patient, 
        'records': records
    })

class DoctorUpdateMedicalRecordView(PermissionRequiredMixin, UpdateView):
    model = MedicalRecord
    fields = ['diagnosis', 'treatment_plan', 'lab_results']
    permission_required = 'health_records.change_MedicalRecord'
    template_name = 'health_records/doctor_update_record.html'
    success_url = '/success/'  # Change this to the appropriate success URL

    def get_queryset(self):
        """Restrict the queryset to allow doctors to edit records of their patients."""
        return MedicalRecord.objects.filter(patient__doctor=self.request.user)
    
@login_required
def view_health_records(request):
    try:
        patient = request.user.patient  # Ensure the user is a patient
    except request.user.patient.RelatedObjectDoesNotExist:
        return render(request, 'health_records/error.html', {
            'error_message': 'You are not registered as a patient.'
        })

    health_records = MedicalRecord.objects.filter(patient=patient)
    return render(request, 'health_records/edit_records.html', {
        'health_records': health_records
    })

def add_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_record_list')  # Redirect to record list
    else:
        form = MedicalRecordForm()
    return render(request, 'health_records/add_medical_record.html', {'form': form})

def download_health_record_csv(request, record_id):
    # Get the specific health record
    record = MedicalRecord.objects.get(id=record_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="health_record_{record_id}.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the headers and data for the health record
    writer.writerow(['Patient', 'Diagnosis', 'Treatment Plan', 'Lab Results', 'Date Created'])
    writer.writerow([record.patient.get_full_name(), record.diagnosis, record.treatment_plan, record.lab_results, record.date_created])

    return response



def download_health_record(request, record_id):
    # Fetch the health record by its ID
    health_record = get_object_or_404(MedicalRecord, id=record_id)

    # Access the patient's name from the CustomUser model
    patient_name = f"{health_record.patient.first_name} {health_record.patient.last_name}"

    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold the elements
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    
    # Title Style
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=24, textColor=colors.HexColor("#00796B"), spaceAfter=12)

    # Text Style
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=12, textColor=colors.black)

    # Adding logo
    logo = 'path/to/your/logo.png'  # Update this path to your logo
    elements.append(Image(logo, width=100, height=50))  # Adjust width and height as needed
    elements.append(Spacer(1, 12))  # Add space after logo

    # Adding title
    elements.append(Paragraph("Health Record", title_style))
    elements.append(Spacer(1, 12))  # Add space between title and patient info

    # Create table data
    data = [
        ["Patient Name:", Paragraph(patient_name, text_style)],
        ["Date of Consultation:", Paragraph(health_record.date_created.strftime('%Y-%m-%d'), text_style)],
        ["Diagnosis:", Paragraph(health_record.diagnosis, text_style)],
        ["Treatment Plan:", Paragraph(health_record.treatment_plan, text_style)],
        ["Lab Results:", Paragraph(health_record.lab_results or 'N/A', text_style)],
    ]

    # Create table and style it
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0F2F1")),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#00796B")),  # Grid lines in teal color
    ]))

    # Add the table to elements
    elements.append(table)

    # Add footer
    elements.append(Spacer(1, 20))  # Space before footer
    elements.append(Paragraph("Thank you for choosing our services!", text_style))

    # Build the PDF
    doc.build(elements)

    # Set the response to be a downloadable PDF
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="health_record_{patient_name}.pdf"'

    # Ensure the buffer is properly closed
    buffer.close()

    return response



