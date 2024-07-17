# doctors/forms.py

from django import forms

from .models import Doctor


class DoctorForm(forms.ModelForm):
    telephone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'tel'}))

    class Meta:
        model = Doctor
        fields = '__all__'
