from django.db import models
from django.contrib.auth.models import User
from Patient.models import PatientProfile


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # For name, email, password
    
    doctor_id = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    specialization = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Dr.{self.user.get_full_name() or self.user.username}"

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date}"

class PatientHistory(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='histories')
    patient_name = models.CharField(max_length=100)
    diagnosis = models.TextField()
    treatment = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.patient_name} - {self.date}"
