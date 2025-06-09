from django import forms
from django.core.exceptions import ValidationError
from .models import Pesticide, Fuel, Seed, PesticideTransaction, FuelTransaction, SeedTransaction

class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['name','active_principle', 'concentration','unit_of_measurement', 'presentation', 
                  'category', 'expiration_date']

        labels = {
            'name': 'Nombre',
            'unit_of_measurement': 'Unidad de medida',
            'presentation': 'Presentación',
            'category': 'Categoría',
            'expiration_date': 'Fecha de vencimiento',
            'active_principle': 'Principio activo',
            'concentration': 'Concentración',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active_principle': forms.TextInput(attrs={'class': 'form-control'}),
            'concentration': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Pesticide.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Ya existe un fitosanitario con ese nombre.")
        return name
    

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name', 'fuel_type', 'supplier', 'unit_of_measurement', 'presentation']

        labels = {
            'name': 'Nombre',
            'fuel_type': 'Tipo de combustible',
            'unit_of_measurement': 'Unidad de medida',
            'presentation': 'Presentación',
            'supplier': 'Proveedor',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Litros'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Bidón 20L'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proveedor'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Fuel.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Ya existe un combustible con ese nombre.")
        return name

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['name','seed_type' ,'category','unit_of_measurement', 'presentation','expiration_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Presentación'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'seed_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de semilla'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Fecha de vencimiento'}),
        }
        labels = {
            'name': 'Nombre',
            'unit_of_measurement': 'Unidad de medida',
            'presentation': 'Presentación',
            'category': 'Categoría',
            'seed_type': 'Tipo de semilla',
            'expiration_date': 'Fecha de vencimiento',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Fuel.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Ya existe una semila con ese nombre.")
        return name

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
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'pesticide': 'Seleccione fitosanitario',
            'observations': 'Observaciones',
            'receipt_number': 'Número de remito',
            'unit_price': 'Precio unitario',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-select'})
        
        
        
        self.fields['unit_price'].required = False
        
        # Agregamos JavaScript para mostrar/ocultar el campo de precio según el tipo de transacción
        self.fields['transaction_type'].widget.attrs['onchange'] = (
            "document.getElementById('div_id_unit_price').style.display = "
            "this.value === 'in' ? 'block' : 'none';"
        )

    
     
    

    def clean(self):
        cleaned_data = super().clean()
        
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        pesticide = cleaned_data.get('pesticide')
        transaction_type = cleaned_data.get('transaction_type')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            # Para entradas, necesitamos un precio
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
        elif transaction_type == 'out':
            # Para salidas, verificamos que el producto tenga stock y precio
            if pesticide:
                if pesticide.available_quantity is None or pesticide.available_quantity <= 0:
                    self.add_error('pesticide', 'Este producto no tiene stock disponible')
                if pesticide.unit_price is None:
                    self.add_error('pesticide', 'Este producto no tiene un precio establecido. Primero debe realizar una entrada.')
                elif quantity > pesticide.available_quantity:
                    self.add_error('quantity', f'La cantidad supera el stock disponible ({pesticide.available_quantity})')
                
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
        # Asigna quantity_in y quantity_out ANTES de llamar a super()._post_clean()
        # para que estas asignaciones se hagan antes de la validación del modelo
        if hasattr(self, 'cleaned_data') and self.cleaned_data:
            transaction_type = self.cleaned_data.get('transaction_type')
            quantity = self.cleaned_data.get('quantity')
            
            if transaction_type == 'in' and quantity:
                self.instance.quantity_in = quantity
                self.instance.quantity_out = 0
            elif transaction_type == 'out' and quantity:
                self.instance.quantity_in = 0
                self.instance.quantity_out = quantity
        
        # Ahora llamamos a super()._post_clean() para que se apliquen las validaciones
        super()._post_clean()
        
def save(self, commit=True):
    instance = super().save(commit=False)

    transaction_type = self.cleaned_data.get('transaction_type')
    quantity = self.cleaned_data.get('quantity')

    if transaction_type == 'in':
        instance.quantity_in = quantity
        instance.quantity_out = 0
        # El unit_price ya fue ingresado por el usuario
    elif transaction_type == 'out':
        instance.quantity_in = 0
        instance.quantity_out = quantity
        # Asignar el precio actual del producto
        instance.unit_price = instance.pesticide.unit_price

    # Calcular el subtotal de la transacción
    instance.subtotal = instance.unit_price * quantity

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
        labels = {
            'fuel': 'Seleccione combustible',
            'observations': 'Observaciones',
            'receipt_number': 'Número de remito',
            'unit_price': 'Precio unitario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['unit_price'].required = False

        self.fields['transaction_type'].widget.attrs['onchange'] = (
            "document.getElementById('div_id_unit_price').style.display = "
            "this.value === 'in' ? 'block' : 'none';"
        )

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        fuel = cleaned_data.get('fuel')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
        elif transaction_type == 'out':
            if fuel:
                if fuel.available_quantity is None or fuel.available_quantity <= 0:
                    self.add_error('fuel', 'Este producto no tiene stock disponible')
                if fuel.unit_price is None:
                    self.add_error('fuel', 'Este producto no tiene un precio establecido. Primero debe realizar una entrada.')
                elif quantity > fuel.available_quantity:
                    self.add_error('quantity', f'La cantidad supera el stock disponible ({fuel.available_quantity})')
                
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
        # Asigna quantity_in y quantity_out ANTES de llamar a super()._post_clean()
        # para que estas asignaciones se hagan antes de la validación del modelo
        if hasattr(self, 'cleaned_data') and self.cleaned_data:
            transaction_type = self.cleaned_data.get('transaction_type')
            quantity = self.cleaned_data.get('quantity')
            
            if transaction_type == 'in' and quantity:
                self.instance.quantity_in = quantity
                self.instance.quantity_out = 0
            elif transaction_type == 'out' and quantity:
                self.instance.quantity_in = 0
                self.instance.quantity_out = quantity
        
        # Ahora llamamos a super()._post_clean() para que se apliquen las validaciones
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
    
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad")
    
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="Tipo de Transacción")
    
    class Meta:
        model = SeedTransaction
        fields = ['seed','unit_price', 'observations', 'receipt_number']
        widgets = {
            'seed': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'unit_price': 'Precio unitario',
            'seed': 'Seleccione semilla',
            'observations': 'Observaciones',
            'receipt_number': 'Número de remito',
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['unit_price'].required = False

        self.fields['transaction_type'].widget.attrs['onchange'] = (
            "document.getElementById('div_id_unit_price').style.display = "
            "this.value === 'in' ? 'block' : 'none';"
        )

        

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        seed = cleaned_data.get('seed')
        
        if not quantity or quantity <= 0:
            self.add_error('quantity', 'La cantidad debe ser mayor a cero')
            
        if transaction_type == 'in':
            if not unit_price or unit_price <= 0:
                self.add_error('unit_price', 'Debe ingresar un precio unitario para las entradas')
        elif transaction_type == 'out':
            if seed:
                if seed.available_quantity is None or seed.available_quantity <= 0:
                    self.add_error('seed', 'Este producto no tiene stock disponible')
                if seed.unit_price is None:
                    self.add_error('seed', 'Este producto no tiene un precio establecido. Primero debe realizar una entrada.')
                elif quantity > seed.available_quantity:
                    self.add_error('quantity', f'La cantidad supera el stock disponible ({seed.available_quantity})')
                
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
        # Asigna quantity_in y quantity_out ANTES de llamar a super()._post_clean()
        # para que estas asignaciones se hagan antes de la validación del modelo
        if hasattr(self, 'cleaned_data') and self.cleaned_data:
            transaction_type = self.cleaned_data.get('transaction_type')
            quantity = self.cleaned_data.get('quantity')
            
            if transaction_type == 'in' and quantity:
                self.instance.quantity_in = quantity
                self.instance.quantity_out = 0
            elif transaction_type == 'out' and quantity:
                self.instance.quantity_in = 0
                self.instance.quantity_out = quantity
        
        # Ahora llamamos a super()._post_clean() para que se apliquen las validaciones
        super()._post_clean()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('transaction_type') == 'out':
            instance.unit_price = instance.seed.unit_price
        
        if commit:
            instance.save()
        
        return instance