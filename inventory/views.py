from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pesticide, Fuel, Seed
from .forms import PesticideForm, FuelForm, SeedForm, PesticideTransactionForm, FuelTransactionForm, SeedTransactionForm

# Vista para listar inventarios de pesticidas, combustibles y semillas
def inventory_list(request):
    # Obtener todos los productos
    pesticides = Pesticide.objects.all()
    fuels = Fuel.objects.all()
    seeds = Seed.objects.all()

    # Calcular los subtotales de cada tipo de producto
    pesticide_subtotals = [(pesticide, pesticide.unit_price * pesticide.available_quantity) for pesticide in pesticides]
    fuel_subtotals = [(fuel, fuel.unit_price * fuel.available_quantity) for fuel in fuels]
    seed_subtotals = [(seed, seed.unit_price * seed.available_quantity) for seed in seeds]

    # Calcular los totales
    total_value_pesticide_usd = sum(subtotal for _, subtotal in pesticide_subtotals)
    total_cost_fuel_usd = sum(subtotal for _, subtotal in fuel_subtotals)
    total_value_seed_usd = sum(subtotal for _, subtotal in seed_subtotals)

    # Preparar el contexto para el template
    context = {
        'pesticide_subtotals': pesticide_subtotals,
        'fuel_subtotals': fuel_subtotals,
        'seed_subtotals': seed_subtotals,
        'total_value_pesticide_usd': total_value_pesticide_usd,
        'total_cost_fuel_usd': total_cost_fuel_usd,
        'total_value_seed_usd': total_value_seed_usd,
    }

    # Renderizar la página
    return render(request, 'inventory/inventory_list.html', context)

# Vista para crear pesticidas
def create_pesticide(request):
    if request.method == 'POST':
        form = PesticideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pesticide created successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error creating pesticide.")
    else:
        form = PesticideForm()

    return render(request, 'inventory/create_pesticide.html', {'form': form})

# Vista para crear combustibles
def create_fuel(request):
    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuel created successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error creating fuel.")
    else:
        form = FuelForm()

    return render(request, 'inventory/create_fuel.html', {'form': form})

# Vista para crear semillas
def create_seed(request):
    if request.method == 'POST':
        form = SeedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seed created successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error creating seed.")
    else:
        form = SeedForm()

    return render(request, 'inventory/create_seed.html', {'form': form})

# Vista para agregar transacciones de pesticidas
def add_pesticide(request):
    if request.method == 'POST':
        form = PesticideTransactionForm(request.POST)
        if form.is_valid():
            pesticide_transaction = form.save()
            messages.success(request, "Pesticide transaction added successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error adding pesticide transaction.")
    else:
        form = PesticideTransactionForm()

    return render(request, 'inventory/add_pesticide.html', {'form': form})

# Vista para agregar transacciones de combustibles
def add_fuel(request):
    if request.method == 'POST':
        form = FuelTransactionForm(request.POST)
        if form.is_valid():
            fuel_transaction = form.save()
            messages.success(request, "Fuel transaction added successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error adding fuel transaction.")
    else:
        form = FuelTransactionForm()

    return render(request, 'inventory/add_fuel.html', {'form': form})

# Vista para agregar transacciones de semillas
def add_seed(request):
    if request.method == 'POST':
        form = SeedTransactionForm(request.POST)
        if form.is_valid():
            seed_transaction = form.save()
            messages.success(request, "Seed transaction added successfully!")
            return redirect('inventory_list')
        else:
            messages.error(request, "Error adding seed transaction.")
    else:
        form = SeedTransactionForm()

    return render(request, 'inventory/add_seed.html', {'form': form})
