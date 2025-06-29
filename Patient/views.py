from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, PatientProfileForm, LoginForm
from Doctor.forms import AppointmentForm
from .models import PatientProfile
from Doctor.models import DoctorProfile, Appointment
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group, User

def generate_patient_id():
    year = now().year
    count = PatientProfile.objects.count() + 1
    return f"PAT{year}{count:04d}"


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = PatientProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.patient_id = generate_patient_id()
            profile.save()

            patient_group, _ = Group.objects.get_or_create(name='patients')
            user.groups.add(patient_group)

            login(request, user)
            return redirect('patient_dashboard', patient_id=profile.patient_id)

    else:
        user_form = UserRegisterForm()
        profile_form = PatientProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        })

def patient_login_view(request):
    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                patient = PatientProfile.objects.get(user=user)
                if patient:
                    print("patient")
                    return redirect('patient_dashboard', patient_id=patient.patient_id)
            else:
                error_message = 'Invalid email or password'
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message
        })

def patient_logout_view(request):
    logout(request)
    return redirect('login')

def home_page_view(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'home.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    patient = get_object_or_404(PatientProfile, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'Doctor/book_appointment.html', {'form': form, 'doctor': doctor})

def appointment_success(request):
    return render(request, 'Doctor/appointment_success.html')

@login_required
def patient_dashboard_view(request, patient_id):
    profile = get_object_or_404(PatientProfile, patient_id=patient_id)
    doctors = DoctorProfile.objects.all()

    if request.user != profile.user:
        return HttpResponseForbidden("You are not allowed to view this page.")

    return render(request, 'patient_dashboard.html', {'profile': profile, 'doctors': doctors})
