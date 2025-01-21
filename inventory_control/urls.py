from django.contrib import admin
from django.urls import path, include
from inventory import views  # Importar views desde la aplicación inventory

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al admin
    path('inventory/', include('inventory.urls')),  # Incluir las URLs de inventory
    path('', views.inventory_list, name='home'),  # Cambiar home a inventory_list
]
