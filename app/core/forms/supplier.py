from django.forms import ModelForm, ImageField, FileInput, DecimalField
from app.core.models import Supplier, Line, Iva, ProductPrice, Customer, PaymentMethod, Company
from django import forms

class LineForm(ModelForm):
    image = forms.ImageField(
        required=False,
        label="Foto de la linea",
        widget=FileInput(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        })
    )

    class Meta:
        model = Line
        fields = ['description', 'image', 'active'] 
        widgets = {
            "description": forms.TextInput(attrs={
                "placeholder": "Ingrese la descripción de la línea",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "active": forms.CheckboxInput(attrs={
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }),
        }
        labels = {
            "description": "Descripción",
            "image": "Imagen (Opcional)",
            "active": "Activo",
        }

class IvaForm(ModelForm):
    value = DecimalField(
        label="Porcentaje (%)",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "placeholder": "Ingrese el porcentaje de IVA (ej. 12.00)",
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        })
    )
    # image = forms.ImageField(
    #     required=False,
    #     label="Imagen (Opcional)",
    #     widget=FileInput(attrs={
    #         "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    #     })
    # )

    class Meta:
        model = Iva
        fields = ['description', 'value', 'active']
        widgets = {
            "description": forms.TextInput(attrs={
                "placeholder": "Ingrese la descripción del IVA",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "active": forms.CheckboxInput(attrs={
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }),
        }
        labels = {
            "description": "Descripción",
            "value": "Porcentaje (%)",
            "active": "Activo",
            #"image": "Imagen (Opcional)",
        }

class ProductPriceForm(ModelForm):
    class Meta:
        model = ProductPrice
        fields = '__all__' 

class CustomerForm(ModelForm):
    image = forms.ImageField(
        required=False,
        label="Foto del Cliente",
        widget=FileInput(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        })
    )

    class Meta:
        model = Customer
        fields = [
            "dni", 
            "first_name", 
            "last_name", 
            "address",
            "gender",
            "date_of_birth",
            "phone", 
            "email",
            "image",
            "active"
        ]
        error_messages = {
            "dni": {
                "unique": "Ya existe un cliente con este DNI.",
            },
        }
        widgets = {
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese DNI del cliente",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre del cliente",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese apellido del cliente",
                    "id": "id_last_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dirección del cliente",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",  # Especificamos que es un campo de fecha
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
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese correo electrónico",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }
        labels = {
            "dni": "DNI",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "address": "Dirección",
            "gender": "Género",
            "date_of_birth": "Fecha de Nacimiento",
            "phone": "Celular",
            "email": "Correo Electrónico",
            "image": "Imagen del Cliente",
            "active": "Activo",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()


class PaymentMethodForm(ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class CompanyForm(ModelForm):
    image = forms.ImageField(
        required=False,
        label="Foto del Empresa",
        widget=FileInput(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        })
    )

    class Meta:
        model = Company
        fields = [
            "dni",
            "name",
            "address",
            "representative",
            "landline",
            "website",
            "email",
            "image",
            "establishment_code",
            "emission_point_code",
            "authorization_number",
            "taxpayer_type",
            "required_to_keep_accounting",
            "active"
        ]  
        widgets = {
            "dni": forms.TextInput(attrs={
                "placeholder": "Ingrese el RUC de la empresa",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "Ingrese el nombre de la empresa",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "address": forms.TextInput(attrs={
                "placeholder": "Ingrese la dirección de la empresa",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "representative": forms.TextInput(attrs={
                "placeholder": "Ingrese el nombre del representante",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "landline": forms.TextInput(attrs={
                "placeholder": "Ingrese el teléfono fijo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "website": forms.TextInput(attrs={
                "placeholder": "Ingrese el sitio web",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Ingrese el correo electrónico",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "establishment_code": forms.TextInput(attrs={
                "placeholder": "Ingrese el código de establecimiento",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "emission_point_code": forms.TextInput(attrs={
                "placeholder": "Ingrese el código de punto de emisión",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "authorization_number": forms.TextInput(attrs={
                "placeholder": "Ingrese el número de autorización",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "taxpayer_type": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "required_to_keep_accounting": forms.CheckboxInput(attrs={
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }),
            "active": forms.CheckboxInput(attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }),
        }
        labels = {
            "dni": "RUC",
            "name": "Nombre de la Empresa",
            "address": "Dirección",
            "representative": "Representante Legal",
            "landline": "Teléfono Fijo",
            "website": "Sitio Web",
            "email": "Correo Electrónico",
            "image": "Imagen de la empresa",
            "establishment_code": "Código de Establecimiento",
            "emission_point_code": "Código de Punto de Emisión",
            "authorization_number": "Número de Autorización",
            "taxpayer_type": "Tipo de Contribuyente",
            "required_to_keep_accounting": "Obligado a Llevar Contabilidad",
            "active": "Activo",
        }


class SupplierForm(ModelForm):
  image = forms.ImageField(required=False, label="Foto del Proveedor", widget=FileInput(attrs={
    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
  }))

  latitude_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)
  longitude_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)
  address_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)

  class Meta:
    model = Supplier
    fields = ['name', 'ruc', 'address', 'phone', 'latitude', 'longitude', 'active', 'image',
              'latitude_hidden', 'longitude_hidden', 'address_hidden']  # Incluye los campos ocultos
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
        "latitude": forms.TextInput(
        attrs={
          "placeholder": "Coordenada: latitud",
          "id": "id_latitude",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "longitude": forms.TextInput(
        attrs={
          "placeholder": "Coordenada: longitud",
          "id": "id_longitude",
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
        "latitude": "Latitud",
        "longitude": "Longitud",
        "state": "Estado",
        "image": "Imagen Del Proveedor",
    }

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        address = cleaned_data.get('address')

        latitude_hidden = cleaned_data.get('latitude_hidden')
        longitude_hidden = cleaned_data.get('longitude_hidden')
        address_hidden = cleaned_data.get('address_hidden')

        if not latitude_hidden or not longitude_hidden:
            # Si no se proporcionaron coordenadas ocultas, valida la dirección visible
            if not address:
                raise forms.ValidationError("Debes ingresar una dirección o seleccionar una ubicación en el mapa.")
        else:
            # Si se proporcionaron coordenadas ocultas, usa esas en lugar de las visibles
            cleaned_data['latitude'] = latitude_hidden
            cleaned_data['longitude'] = longitude_hidden
            cleaned_data['address'] = address_hidden

        return cleaned_data

    def save(self, commit=True):
        supplier = super().save(commit=False)
        if commit:
            supplier.save()
        return supplier

  def clean_name(self):
    name = self.cleaned_data.get("name")
    return name.upper()
