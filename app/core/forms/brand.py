from django.forms import ModelForm, ImageField, FileInput
from app.core.models import Brand
from django.utils import timezone
from django import forms
import datetime


class BrandForm(ModelForm):
  image = forms.ImageField(required=False, label="Foto de Marca", widget=FileInput(attrs={
    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
  }))

  class Meta:
    model = Brand
    fields = ["description", "active", "image"]
    error_messages = {
      "description": {
        "unique": "Ya existe una marca con este nombre.",
      },
    }
    widgets = {
      "description": forms.TextInput(
        attrs={
          "placeholder": "Ingrese descripción del producto",
          "id": "id_description",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "state": forms.CheckboxInput(
        attrs={
          "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        }
      ),
    }
    labels = {
      "description": "Descripción ",
      "state": "Estado",
      "image": "Imagen",
    }

  def clean_description(self):
    description = self.cleaned_data.get("description")
    return description.upper()
