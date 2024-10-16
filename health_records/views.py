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
from reportlab.pdfgen import canvas
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
    return render(request, 'health_records/edical_records.html', {
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

    # Debugging: Print health record details
    print("Health Record Details:")
    print(f"Patient Name: {patient_name}")
    print(f"Date Created: {health_record.date_created}")
    print(f"Diagnosis: {health_record.diagnosis}")
    print(f"Treatment Plan: {health_record.treatment_plan}")
    print(f"Lab Results: {health_record.lab_results}")

    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Title Style
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=26, textColor=colors.HexColor("#00796B"), spaceAfter=12)

    # Section Header Style
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading1'], fontSize=14, textColor=colors.HexColor("#004D40"), spaceAfter=6)

    # Text Style
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=12, textColor=colors.black)

    # Create PDF canvas for custom drawing
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

    # Add logo at the top center
    logo_path = 'static/images/logo.png'  # Update this path to your logo
    pdf_canvas.drawImage(logo_path, 200, 700, width=200, height=80, mask='auto')  # Center logo at top

    # Overlay a semi-transparent rectangle to simulate fading effect
    pdf_canvas.setFillColor(colors.Color(0, 0, 0, 0.05))  # Light black with low alpha
    pdf_canvas.rect(0, 0, letter[0], letter[1], fill=1)  # Full page rectangle

    # Start building the PDF elements
    elements.append(Paragraph("Health Record", title_style))
    elements.append(Spacer(1, 12))  # Add space between title and patient info

    # Section for Patient Information
    elements.append(Paragraph("Patient Information", header_style))
    elements.append(Spacer(1, 6))

    # Create table data for patient info
    patient_data = [
        ["<b>Patient Name:</b>", Paragraph(patient_name, text_style)],
        ["<b>Date of Consultation:</b>", Paragraph(health_record.date_created.strftime('%Y-%m-%d'), text_style)],
    ]
    patient_table = Table(patient_data)
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0F2F1")),  # Light background for header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#00796B")),  # Grid lines
    ]))
    elements.append(patient_table)

    # Section for Medical Information
    elements.append(Spacer(1, 12))  # Add space between sections
    elements.append(Paragraph("Medical Information", header_style))
    elements.append(Spacer(1, 6))

    # Create table data for medical info
    medical_data = [
        ["<b>Diagnosis:</b>", Paragraph(health_record.diagnosis if health_record.diagnosis else 'N/A', text_style)],
        ["<b>Treatment Plan:</b>", Paragraph(health_record.treatment_plan if health_record.treatment_plan else 'N/A', text_style)],
        ["<b>Lab Results:</b>", Paragraph(health_record.lab_results if health_record.lab_results else 'N/A', text_style)],
    ]
    medical_table = Table(medical_data)
    medical_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0F2F1")),  # Light background for header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#00796B")),  # Grid lines
    ]))
    elements.append(medical_table)

    # Footer
    elements.append(Spacer(1, 20))  # Space before footer
    elements.append(Paragraph("Thank you for choosing our services!", text_style))

    # Build the document
    doc.build(elements)

    # Save the canvas and close it
    pdf_canvas.save()

    # Set the response to be a downloadable PDF
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="health_record_{patient_name}.pdf"'

    # Ensure the buffer is properly closed
    buffer.close()

    return response


