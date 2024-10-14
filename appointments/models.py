from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import Doctor, Patient

User = get_user_model()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Scheduled')
    reason = models.TextField(default="No reason provided")
    def clean(self):
        # Check if appointment_date is None
        if self.appointment_date is None:
            raise ValidationError('Appointment date must be provided.')

        # Check if the appointment date is in the past
        if self.appointment_date < timezone.now():
            raise ValidationError('Appointment date cannot be in the past.')

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date}"
