from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.lista_ventas, name="lista"),
    path("nueva/", views.crear_venta, name="crear"),
    path("comisiones/", views.calcular_comisiones, name="comisiones"),
    path("<int:pk>/editar/", views.editar_venta, name="editar"),
    path("<int:pk>/eliminar/", views.eliminar_venta, name="eliminar"),
]