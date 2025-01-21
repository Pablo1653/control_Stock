from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('create_pesticide/', views.create_pesticide, name='create_pesticide'),
    path('create_fuel/', views.create_fuel, name='create_fuel'),
    path('add_pesticide/', views.add_pesticide, name='add_pesticide'),
    path('add_fuel/', views.add_fuel, name='add_fuel'),
]
