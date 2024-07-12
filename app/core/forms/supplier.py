from django.forms import ModelForm, ImageField, FileInput
from app.core.models import Supplier, Line, Iva, ProductPrice, Customer, PaymentMethod, Company
from django import forms

class LineForm(ModelForm):
    class Meta:
        model = Line
        fields = '__all__' 

class IvaForm(ModelForm):
    class Meta:
        model = Iva
        fields = '__all__' 

class ProductPriceForm(ModelForm):
    class Meta:
        model = ProductPrice
        fields = '__all__' 

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__' 

class PaymentMethodForm(ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class SupplierForm(ModelForm):
  image = forms.ImageField(required=False, label="Foto del Proveedor", widget=FileInput(attrs={
    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
  }))

  class Meta:
    model = Supplier
    fields = ["name", "ruc", "address", "phone", "latitude", "longitude", "active", "image"]
    error_messages = {
        "ruc": {
                "unique": "Ya existe un proveedor con este RUC.",
        },
        "name": {
            "unique": "Ya existe un proveedor con este nombre.",
        },
    }
    widgets = {
      "name": forms.TextInput(
        attrs={
          "placeholder": "Ingrese nombre del proveedor",
          "id": "id_name",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "ruc": forms.TextInput(
        attrs={
          "placeholder": "Ingrese DNI del proveedor",
          "id": "id_ruc",  # DNI nomas esta validado
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "address": forms.TextInput(
        attrs={
          "placeholder": "Ingrese dirección del proveedor",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "phone": forms.TextInput(
        attrs={
          "placeholder": "Ingrese número celular",
          "id": "id_phone",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "state": forms.CheckboxInput(
        attrs={
          "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        }
      ),
      "image": forms.FileInput(
        attrs={
          "type": "file",
          "id": "id_image",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
    }
    labels = {
      "name": "Nombre",
      "ruc": "Dni",
      "address": "Dirección",
      "phone": "Celular",
      "state": "Estado",
      "image": "Imagen Del Proveedor",
    }

  def clean_name(self):
    name = self.cleaned_data.get("name")
    return name.upper()
