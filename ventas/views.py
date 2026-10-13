from decimal import Decimal

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ComisionFiltroForm, VentaFiltroForm, VentaForm
from .models import Regla, Vendedor, Venta


def lista_ventas(request):
    form = VentaFiltroForm(request.GET or None)
    ventas = Venta.objects.select_related("vendedor").all()

    if form.is_bound:
        if form.is_valid():
            vendedor = form.cleaned_data.get("vendedor")
            inicio = form.cleaned_data.get("fecha_inicio")
            fin = form.cleaned_data.get("fecha_fin")

            if vendedor:
                ventas = ventas.filter(vendedor=vendedor)

            if inicio:
                ventas = ventas.filter(fecha_venta__gte=inicio)

            if fin:
                ventas = ventas.filter(fecha_venta__lte=fin)
        else:
            ventas = ventas.none()

    total_monto = (
        ventas.aggregate(total=Sum("monto"))["total"]
        or Decimal("0.00")
    )

    return render(
        request,
        "ventas/lista.html",
        {
            "ventas": ventas,
            "filtro_form": form,
            "total_ventas": ventas.count(),
            "total_monto": total_monto,
            "total_vendedores": Vendedor.objects.count(),
            "reglas": Regla.objects.filter(activa=True),
        },
    )


@require_http_methods(["GET", "POST"])
def crear_venta(request):
    form = VentaForm(
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Venta registrada correctamente.",
        )
        return redirect("ventas:lista")

    return render(
        request,
        "ventas/formulario.html",
        {
            "form": form,
            "titulo": "Registrar venta",
        },
    )


@require_http_methods(["GET", "POST"])
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)

    form = VentaForm(
        request.POST if request.method == "POST" else None,
        instance=venta,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Venta actualizada correctamente.",
        )
        return redirect("ventas:lista")

    return render(
        request,
        "ventas/formulario.html",
        {
            "form": form,
            "titulo": "Editar venta",
        },
    )


@require_http_methods(["GET", "POST"])
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)

    if request.method == "POST":
        venta.delete()
        messages.success(
            request,
            "Venta eliminada correctamente.",
        )
        return redirect("ventas:lista")

    return render(
        request,
        "ventas/conf_eliminacion.html",
        {"venta": venta},
    )




@require_http_methods(["GET"])
def calcular_comisiones(request):
    form = ComisionFiltroForm(
        request.GET if request.GET else None
    )

    resumen = []
    detalle = []
    total_ventas = 0
    total_monto = Decimal("0.00")
    total_comisiones = Decimal("0.00")
    calculado = False

    if form.is_bound and form.is_valid():
        calculado = True

        ventas = (
            Venta.objects.filter(
                fecha_venta__range=(
                    form.cleaned_data["fecha_inicio"],
                    form.cleaned_data["fecha_fin"],
                )
            )
            .select_related("vendedor")
            .order_by("vendedor__nombre", "fecha_venta", "pk")
        )

        reglas = list(
            Regla.objects.filter(activa=True)
            .order_by("-monto_minimo", "pk")
        )

        por_vendedor = {}

        for venta in ventas:
            regla = next(
                (
                    regla
                    for regla in reglas
                    if venta.monto >= regla.monto_minimo
                ),
                None,
            )

            porcentaje = (
                regla.porcentaje
                if regla is not None
                else Decimal("0.0000")
            )

            comision = venta.monto * porcentaje

            if venta.vendedor_id not in por_vendedor:
                por_vendedor[venta.vendedor_id] = {
                    "nombre": venta.vendedor.nombre,
                    "cantidad": 0,
                    "monto": Decimal("0.00"),
                    "comision": Decimal("0.00"),
                }

            vendedor = por_vendedor[venta.vendedor_id]
            vendedor["cantidad"] += 1
            vendedor["monto"] += venta.monto
            vendedor["comision"] += comision

            detalle.append({
                "venta": venta,
                "porcentaje": porcentaje * 100,
                "comision": comision,
                "regla": regla,
            })

            total_ventas += 1
            total_monto += venta.monto
            total_comisiones += comision

        resumen = sorted(
            por_vendedor.values(),
            key=lambda vendedor: vendedor["comision"],
            reverse=True,
        )

    return render(
        request,
        "ventas/comisiones.html",
        {
            "form": form,
            "calculado": calculado,
            "resumen": resumen,
            "detalle": detalle,
            "total_ventas": total_ventas,
            "total_monto": total_monto,
            "total_comisiones": total_comisiones,
        },
    )    