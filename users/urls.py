from django.urls import path
from .views import *  # memanggil semua fungsi yang ada di dalam file views

urlpatterns = [
    path('', list_users, name='list_users'),
]
