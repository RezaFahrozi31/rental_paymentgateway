from django.contrib import admin
from django.urls import path, include

from . views import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('blog.urls')),
    # apps
    path('users/', include('users.urls')),
    path('', home, name='home'),
    path('penjadwalan/', penjadwalan, name='penjadwalan'),
    path('kendaraan_tersedia/<str:tgl_penyewaan>/<str:tgl_kembali>/',
         kendaraan_tersedia, name='kendaraan_tersedia'),
    # path('pilih_kendaraan/<int:kendaraan_id>/', pilih_kendaraan, name='pilih_kendaraan'),
    path('pemesanan_kendaraan/<str:no_polisi>/<str:tgl_penyewaan>/<str:tgl_kembali>/',
         pemesanan_kendaraan, name='pemesanan_kendaraan'),
    path('pembayaran/', pembayaran, name='pembayaran'),

    path('pembayaran/<int:transaksi_id>/', pembayaran, name='pembayaran'),
    path('profile/', profile, name='profile'),
    path('profile/edit_profile/', edit_profile, name='edit_profile'),
    # path('transaksi/')
    path('cetak/', cetak, name='cetak'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('get-payment-methods/', get_payment_methods_view,
         name='get_payment_methods'),
    path('create-transaction/', create_transaction, name='create_transaction'),
    path('pembayaran/<str:reference>/',
         pembayaran, name='pembayaran'),
    path('callback/', payment_callback, name='payment_callback'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
