from django import forms
from django.utils import timezone

from .models import Vendedor, Venta


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["vendedor", "fecha_venta", "monto"]

        labels = {
            "vendedor": "Vendedor",
            "fecha_venta": "Fecha de venta",
            "monto": "Monto de la venta",
        }

        widgets = {
            "vendedor": forms.Select(
                attrs={"class": "form-select"}
            ),
            "fecha_venta": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "monto": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "Ejemplo: 900.00",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["fecha_venta"].input_formats = ["%Y-%m-%d"]

        if not self.is_bound and not self.instance.pk:
            self.initial["fecha_venta"] = timezone.localdate()


class ComisionFiltroForm(forms.Form):
    fecha_inicio = forms.DateField(
        label="Fecha inicial",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control",
                "type": "date",
            },
        ),
    )

    fecha_fin = forms.DateField(
        label="Fecha final",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control",
                "type": "date",
            },
        ),
    )

    def clean(self):
        datos = super().clean()

        inicio = datos.get("fecha_inicio")
        fin = datos.get("fecha_fin")

        if inicio and fin and inicio > fin:
            raise forms.ValidationError(
                "La fecha inicial no puede ser posterior a la fecha final."
            )

        return datos

class VentaFiltroForm(forms.Form):
    vendedor = forms.ModelChoiceField(
        label="Vendedor",
        queryset=Vendedor.objects.all(),
        required=False,
        empty_label="Todos los vendedores",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    fecha_inicio = forms.DateField(
        label="Desde",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control",
                "type": "date",
            },
        ),
    )

    fecha_fin = forms.DateField(
        label="Hasta",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control",
                "type": "date",
            },
        ),
    )

    def clean(self):
        datos = super().clean()
        inicio = datos.get("fecha_inicio")
        fin = datos.get("fecha_fin")

        if inicio and fin and inicio > fin:
            raise forms.ValidationError(
                "La fecha inicial no puede ser posterior a la fecha final."
            )

        return datos