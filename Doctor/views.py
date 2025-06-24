from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Doctor.models import DoctorProfile
from Patient.models import PatientProfile
from .forms import AppointmentForm
from .models import Appointment


