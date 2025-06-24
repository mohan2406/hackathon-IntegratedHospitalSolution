from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('dashboard/<str:patient_id>/', views.patient_dashboard_view, name='patient_dashboard'),
    path('login/', views.patient_login_view, name='login'),
    path('logout/', views.patient_logout_view, name='logout'),
]
