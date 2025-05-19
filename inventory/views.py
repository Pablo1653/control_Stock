from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import F
from .models import Pesticide, Fuel, Seed, PesticideTransaction, FuelTransaction, SeedTransaction
from .forms import (
    PesticideForm, FuelForm, SeedForm,
    PesticideTransactionForm, FuelTransactionForm, SeedTransactionForm
)

def inventory_list(request):
    pesticides = Pesticide.objects.all()
    fuels = Fuel.objects.all()
    seeds = Seed.objects.all()

    # Calculamos subtotal para cada pesticida, manejando valores nulos
    pesticide_subtotals = []
    for p in pesticides:
        if p.unit_price is not None and p.available_quantity is not None:
            subtotal = p.unit_price * p.available_quantity
        else:
            subtotal = 0
        pesticide_subtotals.append((p, subtotal))

    # Lo mismo para los demás productos
    fuel_subtotals = []
    for f in fuels:
        if f.unit_price is not None and f.available_quantity is not None:
            subtotal = f.unit_price * f.available_quantity
        else:
            subtotal = 0
        fuel_subtotals.append((f, subtotal))

    seed_subtotals = []
    for s in seeds:
        if s.unit_price is not None and s.available_quantity is not None:
            subtotal = s.unit_price * s.available_quantity
        else:
            subtotal = 0
        seed_subtotals.append((s, subtotal))

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
            pesticide = form.save()
            messages.success(request, f'Pesticida "{pesticide.name}" creado exitosamente. Ahora puede agregar stock mediante una transacción de entrada.')
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
            fuel = form.save()
            messages.success(request, f'Combustible "{fuel.name}" creado exitosamente. Ahora puede agregar stock mediante una transacción de entrada.')
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
            seed = form.save()
            messages.success(request, f'Semilla "{seed.name}" creada exitosamente. Ahora puede agregar stock mediante una transacción de entrada.')
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
                
                # Mensaje más informativo según el tipo de transacción
                if transaction.quantity_in > 0:
                    messages.success(
                        request, 
                        f'Entrada de {transaction.quantity_in} {transaction.pesticide.unit_of_measurement} '
                        f'de {transaction.pesticide.name} registrada correctamente. '
                        f'Stock actual: {transaction.pesticide.available_quantity} {transaction.pesticide.unit_of_measurement}.'
                    )
                else:
                    messages.success(
                        request, 
                        f'Salida de {transaction.quantity_out} {transaction.pesticide.unit_of_measurement} '
                        f'de {transaction.pesticide.name} registrada correctamente. '
                        f'Stock restante: {transaction.pesticide.available_quantity} {transaction.pesticide.unit_of_measurement}.'
                    )
                
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
                
                # Mensaje más informativo según el tipo de transacción
                if transaction.quantity_in > 0:
                    messages.success(
                        request, 
                        f'Entrada de {transaction.quantity_in} {transaction.fuel.unit_of_measurement} '
                        f'de {transaction.fuel.name} registrada correctamente. '
                        f'Stock actual: {transaction.fuel.available_quantity} {transaction.fuel.unit_of_measurement}.'
                    )
                else:
                    messages.success(
                        request, 
                        f'Salida de {transaction.quantity_out} {transaction.fuel.unit_of_measurement} '
                        f'de {transaction.fuel.name} registrada correctamente. '
                        f'Stock restante: {transaction.fuel.available_quantity} {transaction.fuel.unit_of_measurement}.'
                    )
                
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
        form = FuelTransactionForm()
    
    return render(request, 'inventory/add_fuel.html', {'form': form})

def add_seed(request):
    if request.method == 'POST':
        form = SeedTransactionForm(request.POST)
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
                
                # Mensaje más informativo según el tipo de transacción
                if transaction.quantity_in > 0:
                    messages.success(
                        request, 
                        f'Entrada de {transaction.quantity_in} {transaction.seed.unit_of_measurement} '
                        f'de {transaction.seed.name} registrada correctamente. '
                        f'Stock actual: {transaction.seed.available_quantity} {transaction.seed.unit_of_measurement}.'
                    )
                else:
                    messages.success(
                        request, 
                        f'Salida de {transaction.quantity_out} {transaction.seed.unit_of_measurement} '
                        f'de {transaction.seed.name} registrada correctamente. '
                        f'Stock restante: {transaction.seed.available_quantity} {transaction.seed.unit_of_measurement}.'
                    )
                
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