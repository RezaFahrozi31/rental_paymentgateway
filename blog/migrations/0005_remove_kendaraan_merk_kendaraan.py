# Generated by Django 4.2.4 on 2023-09-09 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_kategori_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kendaraan',
            name='merk_kendaraan',
        ),
    ]