from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

class Biodata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_depan = models.CharField(max_length=50, blank=True, null=True)
    nama_belakang = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telp = models.CharField(max_length=15, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)


    class Meta:
        verbose_name_plural ="Biodata"