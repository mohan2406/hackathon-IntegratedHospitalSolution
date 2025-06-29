from django import forms
from django.contrib.auth.models import User
from .models import PatientProfile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password' }), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password' }), label='Confirm Password')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}), label="Email", required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
                raise forms.ValidationError("Passwords don't match.")

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email address is already registered.")
            return email

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'phone_number', 'family_email', 'family_contact_number', 'current_address']

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}), label='Password')
