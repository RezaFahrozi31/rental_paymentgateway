# Generated by Django 4.2.4 on 2023-11-30 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_kendaraan_harga_alter_transaksi_harga_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaksi',
            name='sudah_dikembalikan',
            field=models.BooleanField(default=False),
        ),
    ]
