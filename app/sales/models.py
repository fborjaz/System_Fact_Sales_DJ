from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from app.core.models import Customer,PaymentMethod, Product, Iva

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoice_customers', verbose_name='Cliente')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='invoices_payment', verbose_name='Método Pago')
    issue_date = models.DateTimeField(verbose_name='Fecha Emisión', default=timezone.now)
    subtotal = models.DecimalField(verbose_name='Subtotal', default=0, max_digits=16, decimal_places=2, editable=False)
    iva_percentage = models.ForeignKey(Iva, on_delete=models.PROTECT, related_name='invoices', verbose_name='Porcentaje IVA', default=1)
    discount = models.DecimalField(verbose_name='Descuento', default=0, max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(verbose_name='Total', default=0, max_digits=16, decimal_places=2, editable=False)
    payment = models.DecimalField(verbose_name='Pago', default=0, max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    change = models.DecimalField(verbose_name='Cambio', default=0, max_digits=16, decimal_places=2, editable=False)
    state = models.CharField(verbose_name='Estado', max_length=1, choices=(('F','Factura'),('A','Anulada'),('M','Modificada')), default='F')
    active = models.BooleanField(verbose_name='Activo', default=True)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ('-issue_date',)
        indexes = [models.Index(fields=['issue_date']),]

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()

    def calculate_subtotal(self):
        subtotal = sum(item.subtotal for item in self.detail.all())
        self.subtotal = subtotal
        self.save()
        return subtotal

    def calculate_iva(self):
        self.iva = self.subtotal * (self.iva_percentage.value / 100)
        self.save()
        return self.iva

    def calculate_total(self):
        self.total = self.subtotal + self.iva - self.discount
        self.save()
        return self.total

    def calculate_change(self):
        self.change = self.payment - self.total
        self.save()
        return self.change

    def save(self, *args, **kwargs):
        self.calculate_subtotal()
        self.calculate_iva()
        self.calculate_total()
        self.calculate_change()
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.id} - {self.customer.get_full_name()}"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='detail', verbose_name='Factura')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='invoicedetail_products', verbose_name='Producto')
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price = models.DecimalField(default=0, max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(default=0, max_digits=16, decimal_places=2, editable=False)
    iva_percentage = models.ForeignKey(Iva, on_delete=models.PROTECT, related_name='invoice_details', verbose_name='Porcentaje IVA', default=1)  # Reemplaza 1 por el ID del IVA predeterminado

    class Meta:
        verbose_name = "Factura Detalle"
        verbose_name_plural = "Factura Detalles"

    def calculate_subtotal(self):
        self.subtotal = self.quantity * self.price
        self.save()
        return self.subtotal
    
    def calculate_iva(self):
        self.iva = self.subtotal * (self.iva_percentage.value / 100)  # Calcula el IVA según el porcentaje del objeto Iva
        self.save()
        return self.iva

    def save(self, *args, **kwargs):
        self.calculate_subtotal()
        self.calculate_iva()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.description}"
