from django.contrib import admin
from .models import Vendedor, Regla, Venta


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha_creacion")


@admin.register(Regla)
class ReglaAdmin(admin.ModelAdmin):
    list_display = ("id", "porcentaje_display", "monto_minimo", "activa")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "vendedor", "fecha_venta", "monto")