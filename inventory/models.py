from django.db import models
from django.core.exceptions import ValidationError

# Modelo abstracto base para productos
class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_of_measurement = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    presentation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def update_stock(self, quantity_in=0, quantity_out=0, new_price=None):
        """
        Actualiza el stock y precio del producto:
        - Si es entrada (quantity_in > 0), suma cantidad y actualiza precio unitario.
        - Si es salida (quantity_out > 0), resta cantidad, sin modificar precio.
        """
        if quantity_out > self.available_quantity:
            raise ValidationError(f"No hay suficiente stock para sacar {quantity_out} unidades de {self.name}. Stock disponible: {self.available_quantity}")
        
        if quantity_in > 0:
            # Actualizar precio promedio ponderado
            total_value = self.unit_price * self.available_quantity + new_price * quantity_in
            total_quantity = self.available_quantity + quantity_in
            self.unit_price = total_value / total_quantity
            self.available_quantity = total_quantity
        elif quantity_out > 0:
            self.available_quantity -= quantity_out

        self.save()

# Modelo para los pesticidas
class Pesticide(Product):
    category = models.CharField(max_length=200)
    expiration_date = models.DateField()
    active_principle = models.CharField(max_length=100)
    concentration = models.CharField(max_length=255, default="")

# Modelo para los combustibles
class Fuel(Product):
    supplier = models.CharField(max_length=200)
    fuel_type = models.CharField(max_length=100, default='')

# Modelo para las semillas
class Seed(Product):
    category = models.CharField(max_length=255)
    seed_type = models.CharField(max_length=255)
    expiration_date = models.DateField()

# Modelo abstracto base para transacciones
class Transaction(models.Model):
    quantity_in = models.PositiveIntegerField(default=0)
    quantity_out = models.PositiveIntegerField(default=0)
    observations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.quantity_in > 0 and self.quantity_out > 0:
            raise ValidationError("No se puede registrar entrada y salida en la misma transacción.")
        if self.quantity_in == 0 and self.quantity_out == 0:
            raise ValidationError("Debe ingresar una cantidad para entrada o salida.")

# Transacción para pesticidas
class PesticideTransaction(Transaction):
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio unitario solo para entradas")

    def save(self, *args, **kwargs):
        # Validar cantidad disponible para salida
        self.clean()
        
        if self.quantity_in > 0:
            if self.price is None:
                raise ValidationError("Debe ingresar un precio para la entrada.")
            self.pesticide.update_stock(quantity_in=self.quantity_in, new_price=self.price)
        elif self.quantity_out > 0:
            # Para salida, se usa precio actual del producto, no se actualiza precio ni se ingresa
            self.price = self.pesticide.unit_price
            self.pesticide.update_stock(quantity_out=self.quantity_out)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.pesticide.name}'

# Transacción para combustibles
class FuelTransaction(Transaction):
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio unitario solo para entradas")

    def save(self, *args, **kwargs):
        self.clean()

        if self.quantity_in > 0:
            if self.price is None:
                raise ValidationError("Debe ingresar un precio para la entrada.")
            self.fuel.update_stock(quantity_in=self.quantity_in, new_price=self.price)
        elif self.quantity_out > 0:
            self.price = self.fuel.unit_price
            self.fuel.update_stock(quantity_out=self.quantity_out)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.fuel.name}'

# Transacción para semillas
class SeedTransaction(Transaction):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio unitario solo para entradas")

    def save(self, *args, **kwargs):
        self.clean()

        if self.quantity_in > 0:
            if self.price is None:
                raise ValidationError("Debe ingresar un precio para la entrada.")
            self.seed.update_stock(quantity_in=self.quantity_in, new_price=self.price)
        elif self.quantity_out > 0:
            self.price = self.seed.unit_price
            self.seed.update_stock(quantity_out=self.quantity_out)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.seed.name}'
