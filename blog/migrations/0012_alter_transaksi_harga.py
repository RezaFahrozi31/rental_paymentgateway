# Generated by Django 4.2.4 on 2023-11-02 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_kendaraan_harga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksi',
            name='harga',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
