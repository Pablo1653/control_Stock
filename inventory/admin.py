from django.contrib import admin
from .models import Pesticide, Fuel, PesticideTransaction, FuelTransaction

# Admin para el modelo Pesticide
class PesticideAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available_quantity', 'unit_price', 'expiration_date')
    list_filter = ('category',)  # Eliminamos 'expiration_date'
    search_fields = ('name', 'category')
    ordering = ('name',)

# Admin para el modelo Fuel
class FuelAdmin(admin.ModelAdmin):
    list_display = ('name', 'fuel_type', 'available_quantity', 'unit_price')  # Eliminamos 'expiration_date'
    list_filter = ('fuel_type',)  # Eliminamos 'expiration_date'
    search_fields = ('name', 'fuel_type')
    ordering = ('name',)

# Admin para el modelo PesticideTransaction
class PesticideTransactionAdmin(admin.ModelAdmin):
    list_display = ('pesticide', 'quantity_in', 'quantity_out')  # Eliminamos 'transaction_date'
    list_filter = ('pesticide',)  # Eliminamos 'transaction_date'
    search_fields = ('pesticide__name',)
    ordering = ('pesticide',)  # Cambiamos 'transaction_date' por 'pesticide'

# Admin para el modelo FuelTransaction
class FuelTransactionAdmin(admin.ModelAdmin):
    list_display = ('fuel', 'quantity_in', 'quantity_out')  # Eliminamos 'transaction_date'
    list_filter = ('fuel',)  # Eliminamos 'transaction_date'
    search_fields = ('fuel__name',)
    ordering = ('fuel',)  # Cambiamos 'transaction_date' por 'fuel'

# Registrar los modelos en el admin
admin.site.register(Pesticide, PesticideAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(PesticideTransaction, PesticideTransactionAdmin)
admin.site.register(FuelTransaction, FuelTransactionAdmin)
