from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    specialization = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"
        
# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def clean(self):
        if self.appointment_date < timezone.now():
            raise ValidationError('Appointment date cannot be in the past.')

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow null values

    def __str__(self):
        return f"Record for {self.patient} by {self.doctor}"
