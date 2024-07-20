import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from app.core.models import Product, Iva
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

from proy_sales.utils import custom_serializer, save_audit


class SaleListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'

    def get_queryset(self):
        query = Q()
        q1 = self.request.GET.get('q')
        if q1 is not None:
            query |= Q(id=q1)
            query |= Q(customer__first_name__icontains=q1)
            query |= Q(customer__last_name__icontains=q1)
        return self.model.objects.filter(query).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Ventas'
        context['title2'] = 'Consulta de Ventas'
        context['create_url'] = reverse_lazy('sales:sales_create')
        context['query'] = self.request.GET.get('q', '')
        return context


class SaleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'add_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.all()
        context['iva_percentages'] = Iva.objects.filter(active=True)
        context['detail_sales'] = []
        context['save_url'] = reverse_lazy('sales:sales_create')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                with transaction.atomic():
                    invoice_data = form.cleaned_data
                    invoice_data['state'] = 'F'
                    sale = Invoice.objects.create(**invoice_data)

                    details = json.loads(request.POST['detail'])
                    for detail in details:
                        InvoiceDetail.objects.create(
                            invoice=sale,
                            product_id=detail['id'],
                            quantity=Decimal(detail['quantify']),
                            price=Decimal(detail['price']),
                            iva_percentage=sale.iva_percentage,  # Usar el iva_percentage de la factura
                        )
                        Product.objects.filter(pk=detail['id']).update(stock=F('stock') - Decimal(detail['quantify']))

                    save_audit(request, sale, "A")
                    messages.success(self.request, f"Éxito al registrar la venta F#{sale.id}")
                    return JsonResponse({"msg": "Éxito al registrar la venta Factura"}, status=200)
            except Exception as ex:
                messages.error(self.request, f"Error al registrar la venta: {ex}")
        else:
            messages.error(self.request, f"Error al grabar la venta!!!: {form.errors}.")
        return JsonResponse({"msg": form.errors}, status=400)


class SaleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'change_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.all()
        detail_sale = list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
            "id", "product", "product__description", "quantity", "price", "subtotal", "iva", "iva_percentage"
        ))
        context['detail_sales'] = json.dumps(detail_sale, default=custom_serializer)
        context['save_url'] = reverse_lazy('sales:sales_update', kwargs={"pk": self.object.id})
        context['iva_percentages'] = Iva.objects.filter(active=True)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                with transaction.atomic():
                    sale = self.get_object()
                    invoice_data = form.cleaned_data
                    Invoice.objects.filter(pk=sale.pk).update(**invoice_data)

                    # Eliminar detalles existentes y ajustar el stock
                    for det in sale.detail.all():
                        det.product.stock += det.quantity
                        det.product.save()
                    sale.detail.all().delete()

                    details = json.loads(request.POST['detail'])
                    for detail in details:
                        InvoiceDetail.objects.create(
                            invoice=sale,
                            product_id=detail['id'],
                            quantity=Decimal(detail['quantify']),
                            price=Decimal(detail['price']),
                            iva_percentage=sale.iva_percentage,  # Usar el iva_percentage de la factura
                        )
                        Product.objects.filter(pk=detail['id']).update(stock=F('stock') - Decimal(detail['quantify']))

                    save_audit(request, sale, "M")
                    messages.success(self.request, f"Éxito al modificar la venta F#{sale.id}")
                    return JsonResponse({"msg": "Éxito al modificar la venta Factura"}, status=200)
            except Exception as ex:
                messages.error(self.request, f"Error al modificar la venta: {ex}")
        else:
            messages.error(self.request, f"Error al actualizar la venta!!!: {form.errors}.")
        return JsonResponse({"msg": form.errors}, status=400)
