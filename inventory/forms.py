from django import forms
from .models import Pesticide, Fuel, PesticideTransaction, FuelTransaction

# Formulario para el modelo Pesticide
class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['name', 'category', 'unit_of_measurement', 'unit_price', 'expiration_date', 'available_quantity', 'presentation']
        labels = {
            'name': 'Nombre del pesticida',
            'category': 'Categoría',
            'unit_of_measurement': 'Unidad de medida',
            'unit_price': 'Precio unitario',
            'expiration_date': 'Fecha de vencimiento',
            'available_quantity': 'Cantidad disponible',
            'presentation': 'Forma de presentación',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del pesticida'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Forma de presentación'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Pesticide.objects.filter(name=name).exists():
            raise forms.ValidationError(f"El pesticida con el nombre '{name}' ya existe.")
        return name


# Formulario para el modelo Fuel
class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name_fuel', 'category', 'unit_price', 'expiration_date', 'available_quantity', 'presentation']
        labels = {
            'name_fuel': 'Nombre del combustible',
            'category': 'Categoría',
            'unit_price': 'Precio unitario',
            'expiration_date': 'Fecha de vencimiento',
            'available_quantity': 'Cantidad disponible',
            'presentation': 'Forma de presentación',
        }
        widgets = {
            'name_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del combustible'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Forma de presentación'}),
        }

    def clean_name_fuel(self):
        name_fuel = self.cleaned_data.get('name_fuel')
        if Fuel.objects.filter(name_fuel=name_fuel).exists():
            raise forms.ValidationError(f"El combustible con el nombre '{name_fuel}' ya existe.")
        return name_fuel


# Formulario para las transacciones de pesticidas
class PesticideTransactionForm(forms.ModelForm):
    class Meta:
        model = PesticideTransaction
        fields = ['pesticide', 'quantity_in', 'quantity_out']
        labels = {
            'pesticide': 'Pesticida',
            'quantity_in': 'Cantidad ingresada',
            'quantity_out': 'Cantidad retirada',
        }
        widgets = {
            'pesticide': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad ingresada'}),
            'quantity_out': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad retirada'}),
        }


# Formulario para las transacciones de combustibles
class FuelTransactionForm(forms.ModelForm):
    class Meta:
        model = FuelTransaction
        fields = ['fuel', 'quantity_in', 'quantity_out']
        labels = {
            'fuel': 'Combustible',
            'quantity_in': 'Cantidad ingresada',
            'quantity_out': 'Cantidad retirada',
        }
        widgets = {
            'fuel': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad ingresada'}),
            'quantity_out': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad retirada'}),
        }
