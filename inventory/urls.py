from django.urls import path
from . import views

urlpatterns = [
    # Ruta para listar inventarios
    path('', views.inventory_list, name='inventory_list'),

    # Rutas para crear elementos
    path('create_pesticide/', views.create_pesticide, name='create_pesticide'),
    path('create_fuel/', views.create_fuel, name='create_fuel'),
    path('create_seed/', views.create_seed, name='create_seed'),  # Ruta para crear semillas

    # Rutas para agregar transacciones
    path('add_pesticide/', views.add_pesticide, name='add_pesticide'),
    path('add_fuel/', views.add_fuel, name='add_fuel'),
    path('add_seed/', views.add_seed, name='add_seed'),  # Ruta para agregar transacciones de semillas
]
