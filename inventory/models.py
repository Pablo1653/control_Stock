from django.db import models
from django.core.exceptions import ValidationError

# Base común para productos
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
        if quantity_out > self.available_quantity:
            raise ValidationError(
                f"No hay suficiente stock para retirar {quantity_out} unidades de {self.name}. Stock disponible: {self.available_quantity}"
            )

        if quantity_in > 0:
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

    class Meta:
        abstract = True

    def clean(self):
        if self.quantity_in and self.quantity_out:
            raise ValidationError("No se puede registrar entrada y salida simultáneamente.")
        if not self.quantity_in and not self.quantity_out:
            raise ValidationError("Debe registrar una entrada o salida.")

# Transacciones específicas
class PesticideTransaction(Transaction):
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        print("DEBUG: Iniciando save de PesticideTransaction")
        self.clean()
        print(f"DEBUG: quantity_in={self.quantity_in}, quantity_out={self.quantity_out}, unit_price={self.unit_price}")

        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
            print(f"DEBUG: Actualizando stock para entrada, cantidad: {self.quantity_in}, precio: {self.unit_price}")
            self.pesticide.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        elif self.quantity_out > 0:
            self.unit_price = self.pesticide.unit_price
            print(f"DEBUG: Actualizando stock para salida, cantidad: {self.quantity_out}")
            self.pesticide.update_stock(quantity_out=self.quantity_out)

        super().save(*args, **kwargs)
        print("DEBUG: Guardado exitoso de PesticideTransaction")

class FuelTransaction(Transaction):
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
            self.fuel.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        elif self.quantity_out > 0:
            self.unit_price = self.fuel.unit_price
            self.fuel.update_stock(quantity_out=self.quantity_out)
            super().save(update_fields=['unit_price'])

    def __str__(self):
        return f"{self.fuel.name}: {'Entrada' if self.quantity_in else 'Salida'}"

class SeedTransaction(Transaction):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        if self.quantity_in > 0:
            if not self.unit_price:
                raise ValidationError("Debe ingresar precio para la entrada.")
            self.seed.update_stock(quantity_in=self.quantity_in, new_price=self.unit_price)
        elif self.quantity_out > 0:
            self.unit_price = self.seed.unit_price
            self.seed.update_stock(quantity_out=self.quantity_out)
            super().save(update_fields=['unit_price'])

    def __str__(self):
        return f"{self.seed.name}: {'Entrada' if self.quantity_in else 'Salida'}"
