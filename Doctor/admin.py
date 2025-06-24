from django.contrib import admin
from .models import DoctorProfile, Appointment, PatientHistory

admin.site.register(DoctorProfile)
admin.site.register(Appointment)
admin.site.register(PatientHistory)
