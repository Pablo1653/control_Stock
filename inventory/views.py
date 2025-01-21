from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pesticide, Fuel, PesticideTransaction, FuelTransaction
from .forms import PesticideForm, FuelForm, PesticideTransactionForm, FuelTransactionForm

# Vista para listar inventarios
def inventory_list(request):
    try:
        pesticides = Pesticide.objects.all()
        fuels = Fuel.objects.all()

        # Calcular subtotales y totales
        pesticide_subtotals = [
            (p, round(p.available_quantity * p.unit_price, 2)) for p in pesticides
        ]
        fuel_subtotals = [
            (f, round(f.available_quantity * f.unit_price, 2)) for f in fuels
        ]
        total_value_pesticide_usd = sum(sub[1] for sub in pesticide_subtotals)
        total_cost_fuel_usd = sum(sub[1] for sub in fuel_subtotals)

        # Pasar los datos a la plantilla
        return render(request, 'inventory/inventory_list.html', {
            'pesticide_subtotals': pesticide_subtotals,  # Lista de tuplas (pesticide, subtotal)
            'fuel_subtotals': fuel_subtotals,  # Lista de tuplas (fuel, subtotal)
            'total_value_pesticide_usd': total_value_pesticide_usd,
            'total_cost_fuel_usd': total_cost_fuel_usd,
        })
    except Exception as e:
        # Manejo de error
        messages.error(request, f"Error al cargar los inventarios: {e}")
        return redirect('home')

# Vista para crear un nuevo pesticida
def create_pesticide(request):
    form = PesticideForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, "Pesticida creado exitosamente.")
            return redirect('inventory_list')
        except Exception as e:
            # Manejo de error
            messages.error(request, f"Error al guardar el pesticida: {e}")
    return render(request, 'inventory/create_pesticide.html', {'form': form})

# Vista para crear un nuevo combustible
def create_fuel(request):
    form = FuelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, "Combustible creado exitosamente.")
            return redirect('inventory_list')
        except Exception as e:
            # Manejo de error
            messages.error(request, f"Error al guardar el combustible: {e}")
    return render(request, 'inventory/create_fuel.html', {'form': form})

# Vista para agregar transacciones de pesticidas
def add_pesticide(request):
    form = PesticideTransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            transaction = form.save(commit=False)
            pesticide = transaction.pesticide
            
            # Validar y actualizar la cantidad disponible
            if transaction.quantity_out:
                if transaction.quantity_out > pesticide.available_quantity:
                    messages.error(request, f"No hay suficiente cantidad disponible para la transacción. Disponible: {pesticide.available_quantity}.")
                    return redirect('inventory_list')  # Redirigir en caso de error
                pesticide.available_quantity -= transaction.quantity_out

            if transaction.quantity_in:
                pesticide.available_quantity += transaction.quantity_in

            pesticide.save()
            transaction.save()

            messages.success(request, "Transacción de pesticida registrada exitosamente.")
            return redirect('inventory_list')
        except Exception as e:
            # Manejo de error
            messages.error(request, f"Error al registrar la transacción: {e}")
            return redirect('inventory_list')  # Redirigir también en caso de error
    return render(request, 'inventory/add_pesticide.html', {'form': form})

# Vista para agregar transacciones de combustibles
def add_fuel(request):
    form = FuelTransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            transaction = form.save(commit=False)
            fuel = transaction.fuel
            
            # Validar y actualizar la cantidad disponible
            if transaction.quantity_out:
                if transaction.quantity_out > fuel.available_quantity:
                    messages.error(request, f"No hay suficiente cantidad disponible para la transacción. Disponible: {fuel.available_quantity}.")
                    return redirect('inventory_list')  # Redirigir en caso de error
                fuel.available_quantity -= transaction.quantity_out

            if transaction.quantity_in:
                fuel.available_quantity += transaction.quantity_in

            fuel.save()
            transaction.save()

            messages.success(request, "Transacción de combustible registrada exitosamente.")
            return redirect('inventory_list')
        except Exception as e:
            # Manejo de error
            messages.error(request, f"Error al registrar la transacción: {e}")
            return redirect('inventory_list')  # Redirigir también en caso de error
    return render(request, 'inventory/add_fuel.html', {'form': form})
