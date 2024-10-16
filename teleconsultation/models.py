from django.db import models
from django.conf import settings
from appointments.models import Appointment

class Teleconsultation(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teleconsultations_as_patient")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teleconsultations_as_doctor")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="teleconsultation")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    call_summary = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='ongoing')

    def __str__(self):
        return f"Teleconsultation between {self.patient} and {self.doctor} on {self.start_time}"
