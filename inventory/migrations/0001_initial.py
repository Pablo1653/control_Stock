# Generated by Django 5.1.5 on 2025-05-20 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_of_measurement', models.CharField(max_length=100)),
                ('presentation', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('available_quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supplier', models.CharField(max_length=200)),
                ('fuel_type', models.CharField(default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pesticide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_of_measurement', models.CharField(max_length=100)),
                ('presentation', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('available_quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=200)),
                ('expiration_date', models.DateField()),
                ('active_principle', models.CharField(max_length=100)),
                ('concentration', models.CharField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_of_measurement', models.CharField(max_length=100)),
                ('presentation', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('available_quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=255)),
                ('seed_type', models.CharField(max_length=255)),
                ('expiration_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FuelTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('observations', models.TextField(blank=True, null=True)),
                ('receipt_number', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_email', models.EmailField(max_length=254)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.fuel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PesticideTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('observations', models.TextField(blank=True, null=True)),
                ('receipt_number', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_email', models.EmailField(max_length=254)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pesticide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.pesticide')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeedTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('observations', models.TextField(blank=True, null=True)),
                ('receipt_number', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_email', models.EmailField(max_length=254)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('seed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.seed')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
