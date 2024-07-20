import json
import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.security.models import AuditUser
from django.utils import timezone
from django.db.models.fields.files import ImageFieldFile

phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Caracteres inválidos para un número de teléfono.")
 
def valida_cedula(value):
    cedula = str(value)
    if not cedula.isdigit():
        raise ValidationError('La cédula debe contener solo números.')

    longitud = len(cedula)
    if longitud != 10:
        raise ValidationError('Cantidad de dígitos incorrecta.')

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        digito = int(cedula[i])
        coeficiente = coeficientes[i]
        producto = digito * coeficiente
        if producto > 9:
            producto -= 9
        total += producto

    digito_verificador = (total * 9) % 10
    if digito_verificador != int(cedula[9]):
        raise ValidationError('La cédula no es válida.')
      
def valida_numero_entero_positivo(value):
    if not str(value).isdigit() or int(value) <= 0:
        raise ValidationError('Debe ingresar un número entero positivo válido.')

def valida_numero_flotante_positivo(value):
    try:
        valor_float = float(value)
        if valor_float <= 0:
            raise ValidationError('Debe ingresar un número flotante positivo válido.')
    except ValueError:
        raise ValidationError('Debe ingresar un número flotante válido.')
    

    
def save_audit(request, model, action):
   
    user = request.user

    # Obtain client ip address
    client_address = get_client_ip(request)


    # Registro en tabla Auditora BD
    auditusuariotabla = AuditUser(usuario=user,
                                         tabla=model.__class__.__name__,
                                         registroid=model.id,
                                         accion=action,
                                         fecha=timezone.now().date(),
                                         hora=timezone.now().time(),
                                         estacion=client_address)
    auditusuariotabla.save()


def custom_serializer(obj):
    """
    Serializador personalizado para manejar objetos no serializables como fechas y campos de imagen.
    """
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)  # Convierte Decimal a float para JSON
    elif isinstance(obj, ImageFieldFile):
        return obj.url if obj else None  # Devuelve la URL de la imagen o None si no hay imagen
    elif hasattr(obj, '__dict__'):
        # Serializa objetos con atributos como diccionarios
        return {key: custom_serializer(value) for key, value in obj.__dict__.items() if not key.startswith('_')}  # Excluye atributos privados
    else:
        return json.JSONEncoder.default(json.JSONEncoder(), obj)  # Manejo predeterminado para otros tipos de datos

def save_audit(request, model, action):
    """
    Guarda un registro de auditoría para un modelo dado y una acción.
    """
    user = request.user
    client_address = get_client_ip(request)  # Utiliza una función más general para obtener la IP

    audit_record = AuditUser(
        usuario=user,
        tabla=model.__class__.__name__,
        registroid=model.id,
        accion=action,
        fecha=timezone.now().date(),
        hora=timezone.now().time(),
        estacion=client_address
    )
    audit_record.save()

def get_client_ip(request):
    """
    Obtiene la dirección IP del cliente desde la solicitud.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Obtiene la primera IP si hay varias
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
