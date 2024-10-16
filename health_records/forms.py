from django import forms
from .models import MedicalRecord  # Import your EHR-specific models

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'diagnosis', 'treatment_plan', 'lab_results']  # Update fields here
