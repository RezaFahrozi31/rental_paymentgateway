from django.contrib import admin
from .models import *
# Register your models here.

class KendaraanAdmin(admin.ModelAdmin):
    list_display = ('kategori','no_polisi','nama','type_kendaraan','harga')

admin.site.register(Kendaraan, KendaraanAdmin)

class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('kendaraan','tgl_penyewaan','tgl_kembali','total')

admin.site.register(Transaksi, TransaksiAdmin)

class MonitoringKendaraanAdmin(admin.ModelAdmin):
    list_display = ('kendaraan','no_polisi','km_kendaraan','oli','ban','air_radiator','air_wiper','lampu','tgl_pemeriksaan_kendaraan','tgl_perawatan_kendaraan')

admin.site.register(MonitoringKendaraan, MonitoringKendaraanAdmin)

class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama',)

admin.site.register(Kategori, KategoriAdmin)