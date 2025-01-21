from django.contrib import admin
from .models import Pesticide, Fuel, PesticideTransaction, FuelTransaction

# Admin para el modelo Pesticide
class PesticideAdmin(admin.ModelAdmin):
    # Mostrar los campos relevantes en el listado
    list_display = ('name', 'category', 'available_quantity', 'unit_price', 'expiration_date')
    list_filter = ('category', 'expiration_date')
    search_fields = ('name', 'category')
    ordering = ('name',)


# Admin para el modelo Fuel
class FuelAdmin(admin.ModelAdmin):
    list_display = ('name_fuel', 'category', 'available_quantity', 'unit_price', 'expiration_date')
    list_filter = ('category', 'expiration_date')
    search_fields = ('name_fuel', 'category')
    ordering = ('name_fuel',)


# Admin para el modelo PesticideTransaction
class PesticideTransactionAdmin(admin.ModelAdmin):
    list_display = ('pesticide', 'quantity_in', 'quantity_out', 'transaction_date')
    list_filter = ('pesticide', 'transaction_date')
    search_fields = ('pesticide__name',)
    ordering = ('transaction_date',)


# Admin para el modelo FuelTransaction
class FuelTransactionAdmin(admin.ModelAdmin):
    list_display = ('fuel', 'quantity_in', 'quantity_out', 'transaction_date')
    list_filter = ('fuel', 'transaction_date')
    search_fields = ('fuel__name_fuel',)
    ordering = ('transaction_date',)


# Registrar los modelos en el admin
admin.site.register(Pesticide, PesticideAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(PesticideTransaction, PesticideTransactionAdmin)
admin.site.register(FuelTransaction, FuelTransactionAdmin)
