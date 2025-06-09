from django.db import models
from django.core.exceptions import ValidationError

# Base común para productos
class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_of_measurement = models.CharField(max_length=100)
    presentation = models.CharField(max_length=100)
    # Estos campos ahora son opcionales con null=True, blank=True
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def update_stock(self, quantity_in=0, quantity_out=0, new_price=None):
        # Inicializa available_quantity si es None
        if self.available_quantity is None:
            self.available_quantity = 0

        if quantity_out > 0 and (self.available_quantity is None or quantity_out > self.available_quantity):
            raise ValidationError(
                f"No hay suficiente stock para retirar {quantity_out} unidades de {self.name}. Stock disponible: {self.available_quantity or 0}"
            )

        if quantity_in > 0:
            # Primera entrada de stock
            if self.unit_price is None or self.available_quantity == 0:
                self.unit_price = new_price
                self.available_quantity = quantity_in
            else:
                # Cálculo del precio promedio ponderado
                total_value = self.unit_price * self.available_quantity + new_price * quantity_in
                total_quantity = self.available_quantity + quantity_in
                self.unit_price = total_value / total_quantity
                self.available_quantity = total_quantity
        elif quantity_out > 0:
            self.available_quantity -= quantity_out

        self.save()

# Modelos específicos
class Pesticide(Product):
    category = models.CharField(max_length=200)
    expiration_date = models.DateField()
    active_principle = models.CharField(max_length=100)
    concentration = models.CharField(max_length=255, default="")

class Fuel(Product):
    supplier = models.CharField(max_length=200)
    fuel_type = models.CharField(max_length=100, default='')

class Seed(Product):
    category = models.CharField(max_length=255)
    seed_type = models.CharField(max_length=255)
    expiration_date = models.DateField()

# Transacción base
class Transaction(models.Model):
    quantity_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observations = models.TextField(blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_email = models.EmailField(max_length=254)

    class Meta:
        abstract = True

    def clean(self):
        if self.quantity_in > 0 and self.quantity_out > 0:
            raise ValidationError("No se puede registrar entrada y salida simultáneamente.")
        if not self.quantity_in > 0 and not self.quantity_out > 0:
            raise ValidationError("Debe registrar una entrada o salida.")

# Transacciones específicas
class PesticideTransaction(Transaction):
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   

    def save(self, *args, **kwargs):
        self.clean()
        
        # Para transacciones de entrada, requerir precio
        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
            
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.pesticide.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        
        # Para transacciones de salida
        elif self.quantity_out > 0:
            # Verificar que haya un precio en el producto
            if self.pesticide.unit_price is None:
                raise ValidationError("No se puede retirar producto sin precio establecido. Primero debe realizar una entrada.")
            
            self.unit_price = self.pesticide.unit_price
            
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.pesticide.update_stock(quantity_out=self.quantity_out)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pesticide.name}: {'Entrada' if self.quantity_in else 'Salida'} - Usuario: {self.created_by_email}"
    

class FuelTransaction(Transaction):
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        
        # Para transacciones de entrada, requerir precio
        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
                
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.fuel.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        
        # Para transacciones de salida
        elif self.quantity_out > 0:
            # Verificar que haya un precio en el producto
            if self.fuel.unit_price is None:
                raise ValidationError("No se puede retirar producto sin precio establecido. Primero debe realizar una entrada.")
                
            self.unit_price = self.fuel.unit_price
            
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.fuel.update_stock(quantity_out=self.quantity_out)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fuel.name}: {'Entrada' if self.quantity_in else 'Salida'} - Usuario: {self.created_by_email}"

class SeedTransaction(Transaction):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        
        # Para transacciones de entrada, requerir precio
        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
                
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.seed.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        
        # Para transacciones de salida
        elif self.quantity_out > 0:
            # Verificar que haya un precio en el producto
            if self.seed.unit_price is None:
                raise ValidationError("No se puede retirar producto sin precio establecido. Primero debe realizar una entrada.")
                
            self.unit_price = self.seed.unit_price
            
            # Guardar primero la transacción
            super().save(*args, **kwargs)
            # Luego actualizar el stock
            self.seed.update_stock(quantity_out=self.quantity_out)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.seed.name}: {'Entrada' if self.quantity_in else 'Salida'} - Usuario: {self.created_by_email}"