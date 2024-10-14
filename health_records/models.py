from django.db import models
from users.models import CustomUser
from appointments.models import Appointment

class HealthRecord(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="health_records")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    lab_results = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Record for {self.patient.get_full_name()} on {self.date_created}"
