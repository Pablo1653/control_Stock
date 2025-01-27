from django import forms
from .models import Pesticide, Fuel, PesticideTransaction, FuelTransaction, Seed, SeedTransaction

# Widget común para entradas numéricas
def numeric_input(attrs=None):
    return forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese valor', **(attrs or {})})

# Widget común para entradas de texto
def text_input(attrs=None):
    return forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese valor', **(attrs or {})})

# Función común de validación para verificar existencia en la base de datos
def check_exists(model, field, value):
    if model.objects.filter(**{field: value}).exists():
        raise forms.ValidationError(f"Ya existe un(a) {model.__name__.lower()} con ese nombre.")
    return value

# Formulario para el modelo Pesticide
class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['name', 'category', 'unit_of_measurement', 'unit_price', 'expiration_date', 'available_quantity', 'presentation', 'active_principle', 'concentration']
        labels = {
            'name': 'Nombre del Fitosanitario',
            'category': 'Categoría',
            'unit_of_measurement': 'Unidad de medida',
            'unit_price': 'Precio unitario',
            'expiration_date': 'Fecha de vencimiento',
            'available_quantity': 'Cantidad disponible',
            'presentation': 'Forma de presentación',
            'active_principle': 'Principio activo',
            'concentration': 'Concentración (%)',
        }
        widgets = {
            'name': text_input({'placeholder': 'Nombre del fitosanitario'}),
            'category': text_input({'placeholder': 'Categoría'}),
            'unit_of_measurement': text_input({'placeholder': 'Unidad de medida'}),
            'unit_price': numeric_input(),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_quantity': numeric_input({'placeholder': 'Cantidad disponible'}),
            'presentation': text_input({'placeholder': 'Forma de presentación'}),
            'active_principle': text_input({'placeholder': 'Principio activo'}),
            'concentration': text_input({'placeholder': 'Concentración (%)'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return check_exists(Pesticide, 'name', name)

# Formulario para el modelo Fuel
class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name','fuel_type','supplier', 'unit_of_measurement', 'unit_price', 'available_quantity']
        labels = {
            'name': 'Nombre del combustible',
            'fuel_type': 'Tipo de combustible',
            'supplier': 'Proveedor',
            'unit_of_measurement': 'Unidad de medida',
            'unit_price': 'Precio unitario',
            'available_quantity': 'Cantidad disponible',
        }
        widgets = {
            'name': text_input({'placeholder': 'Nombre del combustible'}),
            'fuel_type': text_input({'placeholder': 'Tipo de combustible'}),
            'supplier': text_input({'placeholder': 'Proveedor'}),
            'unit_of_measurement': text_input({'placeholder': 'Unidad de medida'}),
            'unit_price': numeric_input(),
            'available_quantity': numeric_input({'placeholder': 'Cantidad disponible'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return check_exists(Fuel, 'name', name)

# Formulario para el modelo Seed
class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['name', 'seed_type', 'presentation', 'available_quantity', 'unit_price', 'expiration_date']
        labels = {
            'name': 'Nombre de la semilla',
            'seed_type': 'Tipo de semilla',
            'presentation': 'Forma de presentación',
            'available_quantity': 'Cantidad disponible',
            'unit_price': 'Precio unitario',
            'expiration_date': 'Fecha de vencimiento',
        }
        widgets = {
            'name': text_input({'placeholder': 'Nombre de la semilla'}),
            'seed_type': text_input({'placeholder': 'Tipo de semilla'}),
            'presentation': text_input({'placeholder': 'Forma de presentación'}),
            'available_quantity': numeric_input({'placeholder': 'Cantidad disponible'}),
            'unit_price': numeric_input(),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return check_exists(Seed, 'name', name)

# Formulario para las transacciones de pesticidas
class PesticideTransactionForm(forms.ModelForm):
    class Meta:
        model = PesticideTransaction
        fields = ['pesticide', 'quantity_in', 'quantity_out']
        labels = {
            'pesticide': 'Pesticida',
            'quantity_in': 'Cantidad Ingresada',
            'quantity_out': 'Cantidad salida',
        }
        widgets = {
            'pesticide': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': numeric_input({'placeholder': 'Cantidad ingresada'}),
            'quantity_out': numeric_input({'placeholder': 'Cantidad salida'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_in = cleaned_data.get('quantity_in')
        quantity_out = cleaned_data.get('quantity_out')

        # Validación para asegurar que al menos una cantidad esté presente
        if not quantity_in and not quantity_out:
            raise forms.ValidationError('Debe ingresar una cantidad en "Cantidad Ingresada" o "Cantidad Salida".')

        return cleaned_data

# Formulario para las transacciones de combustibles
class FuelTransactionForm(forms.ModelForm):
    class Meta:
        model = FuelTransaction
        fields = ['fuel', 'quantity_in', 'quantity_out']
        labels = {
            'fuel': 'Combustible',
            'quantity_in': 'Cantidad Ingresada',
            'quantity_out': 'Cantidad Salida',
        }
        widgets = {
            'fuel': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': numeric_input({'placeholder': 'Cantidad Ingresada'}),
            'quantity_out': numeric_input({'placeholder': 'Cantidad Salida'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_in = cleaned_data.get('quantity_in')
        quantity_out = cleaned_data.get('quantity_out')

        # Validación para asegurar que al menos una cantidad esté presente
        if not quantity_in and not quantity_out:
            raise forms.ValidationError('Debe ingresar una cantidad en "Cantidad Ingresada" o "Cantidad Salida".')

        return cleaned_data

# Formulario para las transacciones de semillas
class SeedTransactionForm(forms.ModelForm):
    class Meta:
        model = SeedTransaction
        fields = ['seed', 'quantity_in', 'quantity_out']
        labels = {
            'seed': 'Semilla',
            'quantity_in': 'Cantidad Ingresada',
            'quantity_out': 'Cantidad Salida',
        }
        widgets = {
            'seed': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': numeric_input({'placeholder': 'Cantidad ingresada'}),
            'quantity_out': numeric_input({'placeholder': 'Cantidad Salida'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_in = cleaned_data.get('quantity_in')
        quantity_out = cleaned_data.get('quantity_out')

        # Validación para asegurar que al menos una cantidad esté presente
        if not quantity_in and not quantity_out:
            raise forms.ValidationError('Debe ingresar una cantidad en "Cantidad Ingresada" o "Cantidad Salida".')

        return cleaned_data
