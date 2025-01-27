from django.db import models

# Modelo para los pesticidas
class Pesticide(models.Model):
    id_pesticide = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    unit_of_measurement = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    presentation = models.CharField(max_length=100)
    active_principle = models.CharField(
        max_length=100,
        blank=False,  # No puede estar vacío
        null=False    # No puede ser nulo en la base de datos
    )
    concentration = models.CharField(
        max_length=255,
        blank=False,  # No puede estar vacío
        null=False,   # No puede ser nulo
        default=""    # Valor por defecto vacío
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Modelo para los combustibles
class Fuel(models.Model):
    id_fuel = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    unit_of_measurement = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    supplier = models.CharField(max_length=200)
    fuel_type = models.CharField(max_length=100, default='')
    presentation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Modelo para las semillas
class Seed(models.Model):
    id_seed = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    seed_type = models.CharField(max_length=255)
    presentation = models.CharField(max_length=255)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Modelo para las transacciones de pesticidas
class PesticideTransaction(models.Model):
    id_pesticide_transaction = models.AutoField(primary_key=True)
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)
    quantity_in = models.PositiveIntegerField(default=0)  # Cantidad que entra (entrada)
    quantity_out = models.PositiveIntegerField(default=0)  # Cantidad que sale (salida)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Actualizar cantidad disponible al guardar la transacción
        if self.quantity_in > 0:
            self.pesticide.available_quantity += self.quantity_in
        elif self.quantity_out > 0:
            self.pesticide.available_quantity -= self.quantity_out
        self.pesticide.save()  # Guardar la actualización en el producto
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.pesticide.name}'

# Modelo para las transacciones de combustible
class FuelTransaction(models.Model):
    id_fuel_transaction = models.AutoField(primary_key=True)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    quantity_in = models.PositiveIntegerField(default=0)  # Cantidad que entra (entrada)
    quantity_out = models.PositiveIntegerField(default=0)  # Cantidad que sale (salida)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Actualizar cantidad disponible al guardar la transacción
        if self.quantity_in > 0:
            self.fuel.available_quantity += self.quantity_in
        elif self.quantity_out > 0:
            self.fuel.available_quantity -= self.quantity_out
        self.fuel.save()  # Guardar la actualización en el producto
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.fuel.name}'

# Modelo para las transacciones de semillas
class SeedTransaction(models.Model):
    id_seed_transaction = models.AutoField(primary_key=True)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    quantity_in = models.PositiveIntegerField(default=0)  # Cantidad que entra (entrada)
    quantity_out = models.PositiveIntegerField(default=0)  # Cantidad que sale (salida)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Actualizar cantidad disponible al guardar la transacción
        if self.quantity_in > 0:
            self.seed.available_quantity += self.quantity_in
        elif self.quantity_out > 0:
            self.seed.available_quantity -= self.quantity_out
        self.seed.save()  # Guardar la actualización en el producto
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transacción de {self.seed.name}'
