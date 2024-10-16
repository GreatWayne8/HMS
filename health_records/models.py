from django.db import models
from users.models import CustomUser

class MedicalRecord(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records_as_doctor')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records_as_patient')
    diagnosis = models.CharField(max_length=255, default='Not diagnosed')
    treatment_plan = models.TextField(default='No treatment plan specified')
    lab_results = models.TextField(default='No lab results available')
    
    def __str__(self):
        return f"{self.patient} - {self.diagnosis}"
