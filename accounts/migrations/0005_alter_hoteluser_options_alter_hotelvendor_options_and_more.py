# Generated by Django 5.1.1 on 2024-10-07 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_hotelvendor_business_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hoteluser',
            options={},
        ),
        migrations.AlterModelOptions(
            name='hotelvendor',
            options={},
        ),
        migrations.AlterModelTable(
            name='hoteluser',
            table='hotel_users',
        ),
        migrations.AlterModelTable(
            name='hotelvendor',
            table='hotel_vendors',
        ),
    ]