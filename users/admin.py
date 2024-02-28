from django.contrib import admin
from .models import Biodata

class BiodataAdmin(admin.ModelAdmin):
    list_display = ('user','nama_depan','nama_belakang','telp','alamat')
    

admin.site.register(Biodata, BiodataAdmin)