from django.db import models

# Model for Pesticides
class Pesticide(models.Model):
    id_pesticide = models.AutoField(primary_key=True, verbose_name="Pesticide ID")  # Custom ID
    name = models.CharField(max_length=200, verbose_name="Pesticide Name")
    category = models.CharField(max_length=100, verbose_name="Category")
    unit_of_measurement = models.CharField(max_length=50, verbose_name="Unit of Measurement")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    expiration_date = models.DateField(verbose_name="Expiration Date")
    available_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Available Quantity"
    )
    presentation = models.CharField(
        max_length=100, verbose_name="Presentation", blank=True, null=True
    )  # Updated field name

    class Meta:
        verbose_name = "Pesticide"
        verbose_name_plural = "Pesticides"

    def __str__(self):
        return f"{self.name} ({self.category})"

# Model for Fuels
class Fuel(models.Model):
    id_fuel = models.AutoField(primary_key=True, verbose_name="Fuel ID")  # Custom ID
    name_fuel = models.CharField(max_length=200, verbose_name="Fuel Name")
    category = models.CharField(max_length=100, verbose_name="Category")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    expiration_date = models.DateField(verbose_name="Expiration Date")
    available_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Available Quantity"
    )
    presentation = models.CharField(
        max_length=100, verbose_name="Presentation", blank=True, null=True
    )  # Updated field name

    class Meta:
        verbose_name = "Fuel"
        verbose_name_plural = "Fuels"

    def __str__(self):
        return f"{self.name_fuel} ({self.category})"

# Model for Pesticide Transactions
class PesticideTransaction(models.Model):
    pesticide = models.ForeignKey(
        Pesticide, on_delete=models.CASCADE, related_name="transactions", verbose_name="Pesticide"
    )
    quantity_in = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Quantity In"
    )
    quantity_out = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Quantity Out"
    )
    transaction_date = models.DateField(auto_now_add=True, verbose_name="Transaction Date")

    class Meta:
        verbose_name = "Pesticide Transaction"
        verbose_name_plural = "Pesticide Transactions"

    def __str__(self):
        return f"{self.pesticide.name} - {self.transaction_date}"

# Model for Fuel Transactions
class FuelTransaction(models.Model):
    fuel = models.ForeignKey(
        Fuel, on_delete=models.CASCADE, related_name="transactions", verbose_name="Fuel"
    )
    quantity_in = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Quantity In"
    )
    quantity_out = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Quantity Out"
    )
    transaction_date = models.DateField(auto_now_add=True, verbose_name="Transaction Date")

    class Meta:
        verbose_name = "Fuel Transaction"
        verbose_name_plural = "Fuel Transactions"

    def __str__(self):
        return f"{self.fuel.name_fuel} - {self.transaction_date}"
