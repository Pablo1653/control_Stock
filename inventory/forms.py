from django import forms
from django.core.exceptions import ValidationError
from .models import Pesticide, Fuel, Seed, PesticideTransaction, FuelTransaction, SeedTransaction

class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['name', 'unit_of_measurement', 'unit_price', 'available_quantity',
                  'presentation', 'category', 'expiration_date', 'active_principle', 'concentration']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active_principle': forms.TextInput(attrs={'class': 'form-control'}),
            'concentration': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name', 'unit_of_measurement', 'unit_price', 'available_quantity',
                  'presentation', 'supplier', 'fuel_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['name', 'unit_of_measurement', 'unit_price', 'available_quantity',
                  'presentation', 'category', 'seed_type', 'expiration_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'seed_type': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PesticideTransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="Tipo de Transacción")
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad")
    
    class Meta:
        model = PesticideTransaction
        fields = ['pesticide', 'observations', 'receipt_number', 'unit_price']
        widgets = {
            'pesticide': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Bootstrap a los campos que no están en Meta.widgets
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        
        # Hacemos que unit_price no sea requerido por defecto
        self.fields['unit_price'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            # Para entradas, necesitamos un precio
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
                
        # Agregamos los campos quantity_in y quantity_out a cleaned_data
        if transaction_type == 'in':
            cleaned_data['quantity_in'] = quantity
            cleaned_data['quantity_out'] = 0
        elif transaction_type == 'out':
            cleaned_data['quantity_in'] = 0
            cleaned_data['quantity_out'] = quantity
            
        return cleaned_data

    def _post_clean(self):
        """
        Este método se ejecuta después de clean() y antes de la validación del modelo.
        Vamos a asignar quantity_in y quantity_out antes de que el modelo haga su validación.
        """
        transaction_type = self.cleaned_data.get('transaction_type')
        quantity = self.cleaned_data.get('quantity')
        
        if transaction_type == 'in':
            self.instance.quantity_in = quantity
            self.instance.quantity_out = 0
        elif transaction_type == 'out':
            self.instance.quantity_in = 0
            self.instance.quantity_out = quantity
            
        super()._post_clean()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Para salidas, tomamos el precio unitario del pesticida
        if self.cleaned_data.get('transaction_type') == 'out':
            instance.unit_price = instance.pesticide.unit_price
        
        if commit:
            instance.save()
        
        return instance

class FuelTransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="Tipo de Transacción")
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad")
    
    class Meta:
        model = FuelTransaction
        fields = ['fuel', 'observations', 'receipt_number', 'unit_price']
        widgets = {
            'fuel': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['unit_price'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
                
        # Agregamos los campos quantity_in y quantity_out a cleaned_data
        if transaction_type == 'in':
            cleaned_data['quantity_in'] = quantity
            cleaned_data['quantity_out'] = 0
        elif transaction_type == 'out':
            cleaned_data['quantity_in'] = 0
            cleaned_data['quantity_out'] = quantity
            
        return cleaned_data

    def _post_clean(self):
        transaction_type = self.cleaned_data.get('transaction_type')
        quantity = self.cleaned_data.get('quantity')
        
        if transaction_type == 'in':
            self.instance.quantity_in = quantity
            self.instance.quantity_out = 0
        elif transaction_type == 'out':
            self.instance.quantity_in = 0
            self.instance.quantity_out = quantity
            
        super()._post_clean()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('transaction_type') == 'out':
            instance.unit_price = instance.fuel.unit_price
        
        if commit:
            instance.save()
        
        return instance

class SeedTransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="Tipo de Transacción")
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad")
    
    class Meta:
        model = SeedTransaction
        fields = ['seed', 'observations', 'receipt_number', 'unit_price']
        widgets = {
            'seed': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['unit_price'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
                
        # Agregamos los campos quantity_in y quantity_out a cleaned_data
        if transaction_type == 'in':
            cleaned_data['quantity_in'] = quantity
            cleaned_data['quantity_out'] = 0
        elif transaction_type == 'out':
            cleaned_data['quantity_in'] = 0
            cleaned_data['quantity_out'] = quantity
            
        return cleaned_data

    def _post_clean(self):
        transaction_type = self.cleaned_data.get('transaction_type')
        quantity = self.cleaned_data.get('quantity')
        
        if transaction_type == 'in':
            self.instance.quantity_in = quantity
            self.instance.quantity_out = 0
        elif transaction_type == 'out':
            self.instance.quantity_in = 0
            self.instance.quantity_out = quantity
            
        super()._post_clean()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('transaction_type') == 'out':
            instance.unit_price = instance.seed.unit_price
        
        if commit:
            instance.save()
        
        return instance