from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
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
        


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow null values

    def __str__(self):
        return f"Record for {self.patient} by {self.doctor}"
