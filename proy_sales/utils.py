from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.security.models import AuditUser
from django.utils import timezone

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
    

# class Parameters:
#     LOGO_SYSTEM = '/static/img/iguana_corporation.png'
#     SYSTEM_NAME = 'E-ComPro'

#     # ACTIONS FOR AUDIT TABLES
#     ACTION_ADD = 'A'
#     ACTION_MODIFY = 'M'
#     ACTION_DELETE = 'E'
    
    
def save_audit(request, model, action):
   
    user = request.user

    # Obtain client ip address
    client_address = ip_client_address(request)


    # Registro en tabla Auditora BD
    auditusuariotabla = AuditUser(usuario=user,
                                         tabla=model.__class__.__name__,
                                         registroid=model.id,
                                         accion=action,
                                         fecha=timezone.now().date(),
                                         hora=timezone.now().time(),
                                         estacion=client_address)
    auditusuariotabla.save()


# Obtener el IP desde donde se esta accediendo
def ip_client_address(request):
    try:
        # case server externo
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except:
        # case localhost o 127.0.0.1
        client_address = request.META['REMOTE_ADDR']

    return client_address   
