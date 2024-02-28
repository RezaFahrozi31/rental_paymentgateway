from django.db import models
import datetime
from users.models import Biodata
from django.core.validators import MinValueValidator


class Kategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.nama,)

    class Meta:
        verbose_name_plural = "Kategori"


class Kendaraan(models.Model):
    kategori = models.ForeignKey(
        Kategori, on_delete=models.CASCADE, blank=True, null=True)
    no_polisi = models.CharField(max_length=100, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    type_kendaraan = models.CharField(max_length=100, blank=True, null=True)
    tahun_kendaraan = models.CharField(max_length=20, blank=True, null=True)
    harga = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[(
        'tersedia', 'Tersedia'), ('disewa', 'Disewa')], default='tersedia')

    def __str__(self):
        return "{} - {} - {}".format(self.kategori, self.nama, self.no_polisi)

    class Meta:
        verbose_name_plural = "Kendaraan"


class Transaksi(models.Model):
    kendaraan = models.ForeignKey(
        Kendaraan, on_delete=models.CASCADE, blank=True, null=True)
    tgl_penyewaan = models.DateTimeField(blank=True, null=True)
    tgl_kembali = models.DateTimeField(blank=True, null=True)
    harga = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    sudah_dikembalikan = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.sudah_dikembalikan and self.kendaraan and self.kendaraan.status == 'disewa':
            self.kendaraan.status = 'tersedia'
            self.kendaraan.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.tgl_penyewaan, self.tgl_kembali)

    class Meta:
        verbose_name_plural = "Transaksi"


class MonitoringKendaraan(models.Model):
    kendaraan = models.ForeignKey(
        Kendaraan, on_delete=models.CASCADE, blank=True, null=True)
    no_polisi = models.CharField(max_length=100, blank=True, null=True)
    km_kendaraan = models.CharField(max_length=100, blank=True, null=True)
    oli = models.CharField(max_length=100, blank=True, null=True)
    ban = models.CharField(max_length=100, blank=True, null=True)
    air_radiator = models.CharField(max_length=100, blank=True, null=True)
    air_wiper = models.CharField(max_length=100, blank=True, null=True)
    lampu = models.CharField(max_length=100, blank=True, null=True)
    tgl_pemeriksaan_kendaraan = models.CharField(
        max_length=100, blank=True, null=True)
    tgl_perawatan_kendaraan = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.no_polisi, self.km_kendaraan)

    class Meta:
        verbose_name_plural = "MonitoringKendaraan"


class Pembayaran(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    method = models.CharField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    merchant_ref = models.CharField(max_length=100, blank=True, null=True)
    total_pembayaran = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=[(
        'PENDING', 'PENDING'), ('PAID', 'PAID'), ('EXPIRED', 'EXPIRED')], default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {}".format(self.transaksi, self.method, self.status)
