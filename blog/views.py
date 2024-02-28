from django.shortcuts import render, redirect, get_object_or_404
from re import template
from .forms import *
from users.forms import *
from .models import Kendaraan, Kategori, MonitoringKendaraan, Transaksi, Pembayaran
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse


def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False

@login_required
@user_passes_test(is_operator)
def dashboard(request):
    if request.user.groups.filter(name='Operator').exists():
        request.session['is_operator'] = 'operator'
    template_name = "back/dashboard.html"
    return render(request, template_name)

@login_required
def users(request):
    template_name = "back/tabel_users.html"
    list_user = User.objects.all()
    context = {
        'title':'tabel_user',
        'list_user':list_user,
    }
    return render(request, template_name, context)

@login_required
def tambah_users(request):
    template_name = "back/tambah_users.html"

    if request.method == 'POST':
        user_form = TambahUserForm(request.POST)
        biodata_form = TambahBiodataForm(request.POST)
        if user_form.is_valid() and biodata_form.is_valid():
            # Save User
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data.get('password'))  # Set the password using cleaned_data
            user.save()

            # Save Biodata
            biodata = biodata_form.save(commit=False)
            biodata.user = user
            biodata.save()

            # Authenticate and login user
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            return redirect('tabel_users')

    else:
        user_form = TambahUserForm()
        biodata_form = TambahBiodataForm()

    return render(request, template_name, {'user_form': user_form, 'biodata_form': biodata_form})

@login_required
def hapus_users(request, id):
    User.objects.get(id=id).delete()
    messages.add_message(request, messages.SUCCESS, 'succes delete data')
    return redirect('tabel_users')

@login_required
def edit_users(request,id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('tabel_users')  # Replace with the actual URL name for your user list view
    else:
        user_form = CustomUserChangeForm(instance=user)

    return render(request, 'back/edit_user.html', {'user_form': user_form, 'user': user})


@login_required
def kendaraan(request):
    template_name = "back/tabel_kendaraan.html"
    kendaraan = Kendaraan.objects.all()
    context ={
        'kendaraan':kendaraan,
    }
    return render(request, template_name, context)

@login_required
def tambah_kendaraan(request):
    template_name = "back/tambah_kendaraan.html"
    if request.method == 'POST':
        form = KendaraanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabel_kendaraan')
    else:
        form = KendaraanForm()
    
    return render(request, template_name, {'form': form})

@login_required
def transaksi_back(request):
    template_name = "back/transaksi_back.html"
    transaksi_back = Transaksi.objects.all()
    context = {
        'transaksi_back': transaksi_back,
        }
    return render(request, template_name, context)

@login_required
def tambah_transaksi(request):
    template_name = "back/tambah_transaksi.html"
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaksi_back')  # Change 'transaksi_list' to the name of your transaction list view
    else:
        form = TransaksiForm()

    return render(request, template_name, {'form': form})

@login_required
def konfirmasi_pengembalian(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, pk=transaksi_id)

    if request.method == 'POST':
        # Tambahkan logika untuk mengkonfirmasi pengembalian, misalnya dengan mengubah status
        transaksi.sudah_dikembalikan = True
        transaksi.save()

        messages.success(request, 'Pengembalian kendaraan berhasil dikonfirmasi.')
        return redirect('transaksi_back')  # Ganti 'transaksi_back' dengan nama halaman yang sesuai

    return render(request, 'konfirmasi_pengembalian.html', {'transaksi': transaksi})

@login_required
def lihat_transaksi(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, pk=transaksi_id)
    return render(request, 'back/lihat_transaksi.html', {'transaksi': transaksi})

@login_required
def hapus_transaksi(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, pk=transaksi_id)
    
    if request.method == 'POST':
        transaksi.delete()
        return redirect('transaksi_back')

    return render(request, 'back/hapus_transaksi.html', {'transaksi': transaksi})

from datetime import datetime, timedelta
from django.utils import timezone
from .models import Transaksi, Pembayaran  # Sesuaikan dengan model yang Anda miliki
@login_required
def get_transactions(request):
    print("View diakses!")
    
    current_time = timezone.now()
    one_hour_ago = current_time - timedelta(hours=1)

    transactions = Transaksi.objects.filter(tgl_penyewaan__gte=one_hour_ago)
    events = []

    for transaction in transactions:
        try:
            pembayaran = Pembayaran.objects.get(transaksi=transaction)
            # Ganti 'nama_atribut_anda_di_sini' dengan nama atribut yang benar
            if pembayaran.status == 'PAID':  # Ganti 'nama_atribut_anda_di_sini' dan 'paid' sesuai dengan nilai status yang sesuai
                events.append({
                    'title': f"{transaction.kendaraan} - {transaction.total}",
                    'start': transaction.tgl_penyewaan.strftime('%Y-%m-%dT%H:%M'),
                    'end': transaction.tgl_kembali.strftime('%Y-%m-%dT%H:%M'),
                    'color': 'green',  # Set warna hijau untuk transaksi yang sudah dibayar
                    # Tambahkan lebih banyak field jika diperlukan
                })
            else:
                events.append({
                    'title': f"{transaction.kendaraan} - {transaction.total}",
                    'start': transaction.tgl_penyewaan.strftime('%Y-%m-%dT%H:%M'),
                    'end': transaction.tgl_kembali.strftime('%Y-%m-%dT%H:%M'),
                    # Tambahkan lebih banyak field jika diperlukan
                })
        except Pembayaran.DoesNotExist:
            pass

    print("Events:", events)

    return JsonResponse(events, safe=False)


@login_required
def monitoring(request):
    template_name = "back/monitoring.html"
    monitoring = MonitoringKendaraan.objects.all()
    context = {
        'monitoring':monitoring,
    }
    return render(request, template_name, context)

@login_required
def kategori(request):
    template_name = "back/kategori.html"
    kategori = Kategori.objects.all()
    context ={
        'kategori':kategori,
    }
    return render(request, template_name, context)

@login_required
def cari_kategori(request):
    template_name = "back/kategori.html"
    query = request.GET.get('query')
    if query:
        hasil_pencarian = Kategori.objects.filter(nama__icontains=query)
    else:
        hasil_pencarian = Kategori.objects.all()

    return render(request, template_name, {'kategori': hasil_pencarian})

@login_required
def tambah_kategori(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kategori')
    else:
        form = KategoriForm()
    return render(request, 'back/tambah_kategori.html', {'form': form})

@login_required
def edit_kendaraan(request,id):
    kendaraan = get_object_or_404(Kendaraan, id=id)
    
    if request.method == 'POST':
        form = KendaraanForm(request.POST, instance=kendaraan)
        if form.is_valid():
            form.save()
            return redirect('tabel_kendaraan')  
    else:
        form = KendaraanForm(instance=kendaraan)

    return render(request, 'back/edit_kendaraan.html', {'form': form})

@login_required
def hapus_kendaraan(request, id):
    template_name = "back/hapus_kendaraan.html"
    kendaraan = get_object_or_404(Kendaraan, id=id)
    context = {
        'kendaraan':kendaraan,
    }
    if request.method == 'POST':
        kendaraan.delete()
        return redirect('tabel_kendaraan')
    
    return render(request, template_name, context)

@login_required
def edit_kategori(request, id):
    template_name = "back/edit_kategori.html"
    kategori = get_object_or_404(Kategori, id=id)
    if request.method == 'POST':
        form = EditKategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('kategori')
    else:
        form = EditKategoriForm(instance=kategori)

    return render(request, template_name, {'form': form, 'kategori': kategori})

@login_required
def hapus_kategori(request, id):
    template_name = "back/hapus_kategori.html"
    kategori = get_object_or_404(Kategori, id=id)
    context = {
        'kategori':kategori,
    }
    if request.method == 'POST':
        kategori.delete()
        return redirect('kategori')
    
    return render(request, template_name, context)

@login_required
def tambah_monitoring(request):
    template_name = "back/tambah_monitoring.html"
    if request.method == 'POST':
        form = MonitoringForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monitoring')
    else:
        form = MonitoringForm()
    
    return render(request, template_name, {'form': form})

@login_required
def hapus_monitoring(request, id):
    template_name = "back/hapus_monitoring.html"
    monitoring = get_object_or_404(MonitoringKendaraan, id=id)
    context = {
        'monitoring':monitoring
    }
    if request.method == 'POST':
        monitoring.delete()
        return redirect('monitoring')
    
    return render(request, template_name, context)


@login_required
def lihat_monitoring(request,id):
    template_name = "back/lihat_monitoring.html"
    monitoring = get_object_or_404(MonitoringKendaraan, id=id)
    context = {
        'monitoring':monitoring
    }
    return render(request,template_name,context)


@login_required
def pembayaran_back(request):
    template_name = "back/pembayaran_back.html"
    pembayaran_back = Pembayaran.objects.all()
    context = {
        'pembayaran_back': pembayaran_back,
        }
    return render(request, template_name, context)