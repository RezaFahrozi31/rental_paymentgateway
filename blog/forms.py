from django import forms
from .models import Kategori, Kendaraan, MonitoringKendaraan, Transaksi
from users.models import Biodata
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']

class KendaraanForm(forms.ModelForm):
    class Meta:
        model = Kendaraan
        fields = ['kategori','no_polisi','nama','type_kendaraan','harga']

class EditKategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']

class MonitoringForm(forms.ModelForm):
    class Meta:
        model = MonitoringKendaraan
        fields = ['kendaraan','km_kendaraan','oli','ban','air_radiator','air_wiper','lampu','tgl_pemeriksaan_kendaraan','tgl_perawatan_kendaraan']

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['kendaraan', 'tgl_penyewaan', 'tgl_kembali','harga','total']
        widgets = {
            'tgl_penyewaan': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'tgl_kembali': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class TambahUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class TambahBiodataForm(forms.ModelForm):
    class Meta:
        model = Biodata
        fields = ['nama_depan', 'nama_belakang', 'telp', 'alamat']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)