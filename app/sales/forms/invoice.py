from app.sales.models import Invoice, Iva
from django import forms
from django.forms import ModelChoiceField

class IvaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.description} ({obj.value}%)"


class InvoiceForm(forms.ModelForm):
    iva_percentage = IvaChoiceField(queryset=Iva.objects.filter(active=True), label='Porcentaje de IVA', 
                                   empty_label="Seleccione un porcentaje de IVA")

    class Meta:
        model = Invoice
        fields = ["customer", "payment_method", "issue_date", "discount", "payment", "iva_percentage"]  
        widgets = {
            "customer": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "payment_method": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "issue_date": forms.DateInput(attrs={
                "type": "date",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }, format='%Y-%m-%d'),
            "discount": forms.NumberInput(attrs={
                "placeholder": "Ingrese descuento",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "min": 0,  # Agrega un valor mínimo de 0 para el descuento
            }),
            "payment": forms.NumberInput(attrs={
                "placeholder": "Ingrese pago",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "min": 0,  # Agrega un valor mínimo de 0 para el pago
            }),
        }
        labels = {
            "customer": "Cliente",
            "payment_method": "Método de Pago",
            "issue_date": "Fecha de Emisión",
            "discount": "Descuento",
            "payment": "Pago",
            "iva_percentage": "Porcentaje de IVA",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos calculados (subtotal, iva, total, cambio) no se muestren en el formulario
        for field_name in ['subtotal', 'iva', 'total', 'change']:
            self.fields[field_name].widget = forms.HiddenInput()
