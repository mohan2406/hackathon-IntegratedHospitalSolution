from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class PatientProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=20, unique=True, editable=False) # custom ID
    name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=15)
    family_email = models.EmailField()
    family_contact_number = models.CharField(max_length=15)
    current_address = models.TextField()

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} - {self.user.username}"
