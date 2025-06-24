from django.urls import path
from . import views
import Patient

urlpatterns = [
        path('book/<int:doctor_id>/', Patient.views.book_appointment, name="book_appointment"),
        path('book/appointment_success/', Patient.views.appointment_success, name="appointment_success")
        ]
