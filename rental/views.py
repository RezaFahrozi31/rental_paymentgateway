from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from blog.models import Kendaraan, Transaksi, Pembayaran
from users.models import Biodata
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from blog.forms import TransaksiForm
from django.db.models import Sum
from django.contrib import messages
from users.models import Biodata
from django import template
from django.contrib.auth.models import Group, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .tripay_helper import *
import json

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False


def home(request):
    template_name = 'front/home.html'
    return render(request, template_name)


def profile(request):
    current_user_biodata = Biodata.objects.get(user=request.user)
    return render(request, 'front/profile.html', {'biodata': current_user_biodata})


def edit_profile(request):
    if request.method == 'POST':
        # Mengambil instance Biodata berdasarkan user yang sedang login
        biodata_edit = Biodata.objects.get(user=request.user)

        # Memperbarui nilai-nilai berdasarkan data yang diterima dari form
        biodata_edit.nama_depan = request.POST.get('nama_depan', '')
        biodata_edit.nama_belakang = request.POST.get('nama_belakang', '')
        biodata_edit.email = request.POST.get('email', '')
        biodata_edit.telp = request.POST.get('telp', '')
        biodata_edit.alamat = request.POST.get('alamat', '')

        # Menyimpan perubahan ke database
        biodata_edit.save()

        messages.success(request, 'Profil berhasil diperbarui!')
        # Ganti 'profile' dengan nama URL untuk menampilkan profil
        return redirect('profile')

    else:
        # Jika request adalah GET, tampilkan form edit profil
        biodata = Biodata.objects.get(user=request.user)
        return render(request, 'edit_profile.html', {'biodata': biodata})


def penjadwalan(request):
    template_name = "front/penjadwalan.html"
    if request.method == 'POST':
        tgl_penyewaan = request.POST['tgl_penyewaan']
        tgl_kembali = request.POST['tgl_kembali']
        # Di sini Anda dapat melakukan validasi tanggal penyewaan dan kembali jika diperlukan
        return redirect('kendaraan_tersedia', tgl_penyewaan=tgl_penyewaan, tgl_kembali=tgl_kembali)
    return render(request, template_name)


def kendaraan_tersedia(request, tgl_penyewaan, tgl_kembali):
    template_name = "front/kendaraan_tersedia.html"
    # Filter transaksi yang belum dibayar (status != 'PAID')
    data_transaksi = Transaksi.objects.filter(
        Q(tgl_penyewaan__lte=tgl_penyewaan, tgl_kembali__gte=tgl_penyewaan) |
        Q(tgl_penyewaan__lte=tgl_kembali, tgl_kembali__gte=tgl_kembali) |
        Q(tgl_penyewaan__gte=tgl_penyewaan, tgl_kembali__lte=tgl_kembali),
        ~Q(pembayaran__status='PAID')
    )

    kendaraan_tersedia = Kendaraan.objects.exclude(
        id__in=data_transaksi.values_list('kendaraan', flat=True))

    context = {
        'data_transaksi': data_transaksi,
        'kendaraan_tersedia': kendaraan_tersedia,
        # 'kendaraan_terpilih': kendaraan_terpilih,
        'tgl_penyewaan': tgl_penyewaan,
        'tgl_kembali': tgl_kembali,
    }

    return render(request, template_name, context)


# views.py

# @login_required
def pemesanan_kendaraan(request, no_polisi, tgl_penyewaan, tgl_kembali):
    template_name = "front/pemesanan.html"
    kendaraan_terpilih = Kendaraan.objects.get(no_polisi=no_polisi)
    tgl_penyewaan_obj = datetime.strptime(tgl_penyewaan, "%Y-%m-%dT%H:%M")
    tgl_kembali_obj = datetime.strptime(tgl_kembali, "%Y-%m-%dT%H:%M")
    selisih_hari = (tgl_kembali_obj - tgl_penyewaan_obj).days
    # Konversi Decimal ke float
    harga_kendaraan = float(kendaraan_terpilih.harga)
    # convert harga_kendaraan ke idr
    harga_kendaraan = int(harga_kendaraan) * 1000
    total_biaya = harga_kendaraan * selisih_hari

    # Simpan data pemesanan ke sesi untuk digunakan saat pembayaran
    request.session['pemesanan_data'] = {
        'no_polisi': no_polisi,
        'tgl_penyewaan': tgl_penyewaan,
        'tgl_kembali': tgl_kembali,
        'kendaraan_terpilih': {
            'nama': kendaraan_terpilih.nama,
            'harga': harga_kendaraan,
            'no_polisi': kendaraan_terpilih.no_polisi,
        },
        'total_biaya': total_biaya,
    }

    context = {
        'tgl_penyewaan': tgl_penyewaan,
        'tgl_kembali': tgl_kembali,
        'kendaraan_terpilih': kendaraan_terpilih,
        'total_biaya': total_biaya,
    }

    return render(request, template_name, context)


@login_required
def create_transaction(request):
    # Ambil data pemesanan dari sesi
    pemesanan_data = request.session.get('pemesanan_data')

    if not pemesanan_data:
        return JsonResponse({'error': 'Data pemesanan tidak ditemukan.'})

    # Ambil informasi pengguna yang login
    current_user = request.user
    current_user_email = current_user.email
    current_user_phone = current_user.biodata.telp

    # Tambahkan informasi pengguna ke data pemesanan
    pemesanan_data['customer_name'] = current_user.get_full_name()
    pemesanan_data['customer_email'] = current_user_email
    pemesanan_data['customer_phone'] = current_user_phone
    # ambil data dari form
    pemesanan_data['payment_method'] = request.POST.get('payment_method')
    transaksi = store_transaction(pemesanan_data)

    if transaksi:
        # create transaksi
        transaksi_instance = Transaksi.objects.create(
            kendaraan=Kendaraan.objects.get(
                no_polisi=pemesanan_data['no_polisi']),
            tgl_penyewaan=pemesanan_data['tgl_penyewaan'],
            tgl_kembali=pemesanan_data['tgl_kembali'],
            harga=pemesanan_data['kendaraan_terpilih']['harga'],
            total=pemesanan_data['total_biaya'],
        )
        # create pembayaran
        pembayaran_instance = Pembayaran.objects.create(
            transaksi=transaksi_instance,  # Linking to the created Transaksi instance
            # ['data']['method'] is the payment method
            method=transaksi['data']['payment_method'],
            reference=transaksi['data']['reference'],
            merchant_ref=transaksi['data']['merchant_ref'],
            total_pembayaran=pemesanan_data['total_biaya'],
        )

        reference = transaksi['data']['reference']
        redirect_url = f'/pembayaran/{reference}/'
        return JsonResponse({'redirect_url': redirect_url}, status=200)
    else:
        return JsonResponse({'error': 'Gagal membuat transaksi.'})


@login_required
def pembayaran(requests, reference):
    template_name = "front/transaksi.html"
    transaksi = get_transaction_detail(reference)

    return render(requests, template_name, {'transaksi': transaksi})


@csrf_exempt  # Important: To disable CSRF protection for this view
def payment_callback(request):
    if request.method == 'POST':
        # Handle the callback data
        try:
            # Verify the callback signature for security
            if not verify_callback_signature(request):
                return JsonResponse({'status': 'error', 'message': 'Invalid signature'})

            data = json.loads(request.body.decode('utf-8'))
            # Ambil data reference dari callback
            reference = data['reference']
            # Ambil data status dari callback
            status = data['status']
            # update status pembayaran
            pembayaran = Pembayaran.objects.get(reference=reference)
            pembayaran.status = status
            pembayaran.save()

            return JsonResponse({'status': 'success', 'message': 'Callback successful'})

        except Pembayaran.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pembayaran not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def hitung_total_biaya(kendaraan_terpilih, tgl_penyewaan, tgl_kembali):
    try:
        tgl_penyewaan = datetime.strptime(tgl_penyewaan, "%Y-%m-%dT%H:%M")
        tgl_kembali = datetime.strptime(tgl_kembali, "%Y-%m-%dT%H:%M")
    except ValueError:
        # Tangani kesalahan jika format tanggal tidak valid
        return None

    # Menghitung jumlah hari penyewaan
    jumlah_hari = (tgl_kembali - tgl_penyewaan).days

    if jumlah_hari < 0:
        # Tangani kesalahan jika tanggal kembali lebih awal daripada tanggal penyewaan
        return None

    # Menghitung total biaya (harga sewa per hari * jumlah hari)
    total_biaya = kendaraan_terpilih.kendaraan.harga * jumlah_hari

    return total_biaya


def get_payment_methods_view(request):
    payment_methods = get_payment_methods()
    return payment_methods


def hitung_total_pembayaran(transaksi_id):
    try:
        transaksi = Transaksi.objects.get(id=transaksi_id)
        total_pembayaran = sum(
            kendaraan.harga for kendaraan in transaksi.kendaraan.all())
        return total_pembayaran
    except Transaksi.DoesNotExist:
        # Handle the case where the transaction does not exist
        return None


def cetak(request):
    template_name = 'front/cetak.html'
    return render(request, template_name)


def login(request):
    if request.user.is_authenticated:
        print('sudah login')
        return redirect('home')

    template_name = 'account/login.html'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('username benar')
            auth_login(request, user)
            return redirect('home')
        else:
            print('username salah')
    context = {
        'title': 'form login'
    }
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    template_name = "account/register.html"
    if request.method == 'POST':
        # Ambil data dari request.POST
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        nama_depan = request.POST['nama_depan']
        nama_belakang = request.POST['nama_belakang']
        telp = request.POST['telp']
        alamat = request.POST['alamat']

        # Buat objek User baru
        user = User.objects.create_user(
            username=username, first_name=nama_depan, last_name=nama_belakang, password=password, email=email)

        # Buat objek Biodata baru dan hubungkan dengan User
        biodata = Biodata(user=user, nama_depan=nama_depan,
                          nama_belakang=nama_belakang, telp=telp, alamat=alamat)
        biodata.save()

        # Redirect ke halaman login atau halaman lain setelah pendaftaran berhasil
        return redirect('home')

    return render(request, template_name)
