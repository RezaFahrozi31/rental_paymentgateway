# Generated by Django 4.2.4 on 2023-11-15 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_pembayaran'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kendaraan',
            name='harga',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='harga',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
