from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Vendedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Vendedores"

    def __str__(self):
        return self.nombre


class Regla(models.Model):
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
        help_text="Ingresa 0.06 para representar el 6 %.",
    )
    monto_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["monto_minimo", "pk"]
        verbose_name = "Regla de comisión"
        verbose_name_plural = "Reglas de comisión"

    @property
    def porcentaje_display(self):
        return f"{self.porcentaje * 100:.2f} %"

    def __str__(self):
        return (
            f"{self.porcentaje_display} "
            f"desde ${self.monto_minimo:.2f}"
        )


class Venta(models.Model):
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name="ventas",
    )
    fecha_venta = models.DateField()
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_venta", "-pk"]

    def __str__(self):
        return (
            f"{self.vendedor.nombre} — "
            f"${self.monto:.2f} ({self.fecha_venta})"
        )

    def calcular_comision(self):
        regla = (
            Regla.objects.filter(
                activa=True,
                monto_minimo__lte=self.monto,
            )
            .order_by("-monto_minimo", "pk")
            .first()
        )

        if regla is None:
            return {
                "comision": Decimal("0.00"),
                "regla_aplicada": None,
                "porcentaje": Decimal("0.0000"),
            }

        return {
            "comision": self.monto * regla.porcentaje,
            "regla_aplicada": regla,
            "porcentaje": regla.porcentaje,
        }