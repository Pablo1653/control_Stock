from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Pesticide, Fuel, Seed, PesticideTransaction, FuelTransaction, SeedTransaction
from .forms import (
    PesticideForm, FuelForm, SeedForm,
    PesticideTransactionForm, FuelTransactionForm, SeedTransactionForm
)

def inventory_list(request):
    pesticides = Pesticide.objects.all()
    fuels = Fuel.objects.all()
    seeds = Seed.objects.all()

    # Calculamos subtotal para cada pesticida: precio unitario * cantidad disponible
    pesticide_subtotals = [(p, p.unit_price * p.available_quantity) for p in pesticides]
    fuel_subtotals = [(f, f.unit_price * f.available_quantity) for f in fuels]
    seed_subtotals = [(s, s.unit_price * s.available_quantity) for s in seeds]

    # Totales generales
    total_pesticides = sum(subtotal for _, subtotal in pesticide_subtotals)
    total_fuels = sum(subtotal for _, subtotal in fuel_subtotals)
    total_seeds = sum(subtotal for _, subtotal in seed_subtotals)

    return render(request, 'inventory/inventory_list.html', {
        'pesticide_subtotals': pesticide_subtotals,
        'fuel_subtotals': fuel_subtotals,
        'seed_subtotals': seed_subtotals,
        'total_pesticides': total_pesticides,
        'total_fuels': total_fuels,
        'total_seeds': total_seeds,
    })

def create_pesticide(request):
    if request.method == 'POST':
        form = PesticideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pesticida creado exitosamente.')
            return redirect('inventory_list')
        else:
            messages.error(request, 'Error al crear el pesticida.')
    else:
        form = PesticideForm()
    return render(request, 'inventory/create_pesticide.html', {'form': form})

def create_fuel(request):
    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Combustible creado exitosamente.')
            return redirect('inventory_list')
        else:
            messages.error(request, 'Error al crear el combustible.')
    else:
        form = FuelForm()
    return render(request, 'inventory/create_fuel.html', {'form': form})

def create_seed(request):
    if request.method == 'POST':
        form = SeedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semilla creada exitosamente.')
            return redirect('inventory_list')
        else:
            messages.error(request, 'Error al crear la semilla.')
    else:
        form = SeedForm()
    return render(request, 'inventory/create_seed.html', {'form': form})

def add_pesticide(request):
    if request.method == 'POST':
        form = PesticideTransactionForm(request.POST)
        # Más información sobre los errores para depuración
        print("DEBUG: POST recibido con data:", request.POST)
        print("DEBUG: ¿Formulario válido?", form.is_valid())
        if not form.is_valid():
            print("DEBUG: Errores del formulario:", form.errors)
        
        if form.is_valid():
            try:
                print("DEBUG: Intentando guardar formulario")
                transaction = form.save()
                print("DEBUG: Guardado exitoso, ID:", transaction.id)
                messages.success(request, 'Transacción de pesticida registrada correctamente.')
                return redirect('inventory_list')
            except ValidationError as e:
                print("DEBUG: Error de validación:", e.messages if hasattr(e, 'messages') else str(e))
                messages.error(request, f'Error de validación: {e.messages if hasattr(e, "messages") else str(e)}')
            except Exception as e:
                print("DEBUG: Error inesperado:", str(e))
                messages.error(request, f'Error inesperado: {str(e)}')
        else:
            print("DEBUG: Formulario no válido, errores:", form.errors)
            # Mensaje de error más específico basado en los errores del formulario
            error_msg = "Por favor corrija los siguientes errores: "
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                error_msg += f"{field_name}: {', '.join(errors)}. "
            messages.error(request, error_msg)
    else:
        form = PesticideTransactionForm()
    
    return render(request, 'inventory/add_pesticide.html', {'form': form})

def add_fuel(request):
    if request.method == 'POST':
        form = FuelTransactionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Transacción de combustible registrada correctamente.')
                return redirect('inventory_list')
            except ValidationError as e:
                messages.error(request, e.message if hasattr(e, 'message') else str(e))
        else:
            error_msg = "Por favor corrija los siguientes errores: "
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                error_msg += f"{field_name}: {', '.join(errors)}. "
            messages.error(request, error_msg)
    else:
        form = FuelTransactionForm()
    return render(request, 'inventory/add_fuel.html', {'form': form})

def add_seed(request):
    if request.method == 'POST':
        form = SeedTransactionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Transacción de semilla registrada correctamente.')
                return redirect('inventory_list')
            except ValidationError as e:
                messages.error(request, e.message if hasattr(e, 'message') else str(e))
        else:
            error_msg = "Por favor corrija los siguientes errores: "
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                error_msg += f"{field_name}: {', '.join(errors)}. "
            messages.error(request, error_msg)
    else:
        form = SeedTransactionForm()
    return render(request, 'inventory/add_seed.html', {'form': form})

def pesticide_movements(request):
    transactions = PesticideTransaction.objects.select_related('pesticide')
    return render(request, 'inventory/pesticide_movements.html', {'transactions': transactions})

def fuel_movements(request):
    transactions = FuelTransaction.objects.select_related('fuel')
    return render(request, 'inventory/fuel_movements.html', {'transactions': transactions})

def seed_movements(request):
    transactions = SeedTransaction.objects.select_related('seed')
    return render(request, 'inventory/seed_movements.html', {'transactions': transactions})