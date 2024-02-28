from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Biodata

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Biodata
        fields = ['user', 'nama_depan', 'nama_belakang', 'email', 'telp', 'alamat']
