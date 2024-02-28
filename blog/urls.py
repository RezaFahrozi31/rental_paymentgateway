from django.urls import path, include
from . views import *

urlpatterns = [
    path('dashboard',dashboard, name='dashboard'),
    path('users/',users, name='tabel_users'),
    path('kendaraan/',kendaraan, name='tabel_kendaraan'),
    path('transaksi_back/',transaksi_back, name='transaksi_back'),
    path('monitoring/',monitoring, name='monitoring'),
    path('monitoring/tambah_monitoring/',tambah_monitoring, name='tambah_monitoring'),
    path('monitoring/hapus_monitoring/<str:id>',hapus_monitoring, name='hapus_monitoring'),
    path('monitoring/lihat_monitoring/<str:id>',lihat_monitoring, name='lihat_monitoring'),
    path('kategori/',kategori, name='kategori'),
    path('kategori/cari_kategori/',cari_kategori, name='cari_kategori'),
    path('kategori/tambah_kategori/',tambah_kategori, name='tambah_kategori'),
    path('kategori/edit_kategori/<str:id>/',edit_kategori, name='edit_kategori'),
    path('kategori/hapus_kategori/<str:id>/',hapus_kategori, name='hapus_kategori'),
    path('kendaraan/tambah_kendaraan/',tambah_kendaraan, name='tambah_kendaraan'),
    path('kendaraan/edit_kendaraan/<str:id>/',edit_kendaraan, name='edit_kendaraan'),
    path('kendaraan/hapus_kendaraan/<str:id>/',hapus_kendaraan, name='hapus_kendaraan'),
    path('tambah_transaksi/',tambah_transaksi, name='tambah_transaksi'),
    path('users/tambah_users',tambah_users, name='tambah_users'),
    path('users/hapus_users/<int:id>/',hapus_users, name='hapus_users'),
    path('users/edit_users/<int:id>/', edit_users, name='edit_users'),
    path('konfirmasi_pengembalian/<int:transaksi_id>/', konfirmasi_pengembalian, name='konfirmasi_pengembalian'),
    path('transaksi_back/lihat_transaksi/<int:transaksi_id>/', lihat_transaksi, name='lihat_transaksi'),
    path('transaksi_back/hapus_transaksi/<int:transaksi_id>/', hapus_transaksi, name='hapus_transaksi'),
    path('get_transactions/', get_transactions, name='get_transactions'),
    path('pembayaran_back/', pembayaran_back, name='pembayaran_back'),


]