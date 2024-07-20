from io import BytesIO
import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from django.utils import timezone
from app.core.forms.supplier import SupplierForm
from app.core.models import Product, Company
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View, TemplateView
from django.contrib import messages
from django.db.models import Q,F
from decimal import Decimal
from datetime import timedelta
from proy_sales import settings
from proy_sales.utils import custom_serializer, save_audit
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


class SaleListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(id = q1), Q.OR) 
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR) 
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SaleCreateView(PermissionMixin,CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'add_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        context['detail_sales'] =[]
        context['save_url'] = reverse_lazy('sales:sales_create') 
        print(context['products'])
        
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request received")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al grabar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            with transaction.atomic():
                sale = Invoice.objects.create(
                    customer_id=int(data['customer']),
                    payment_method_id=int(data['payment_method']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    discount=Decimal(data['discount']),
                    iva= Decimal(data['iva']),
                    total=Decimal(data['total']),
                    payment=Decimal(data['payment']),
                    change=Decimal(data['change']),
                    state='N'
                )
                details = json.loads(request.POST['detail'])
                print(details) #[{'id':'1','price':'2'},{}]
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "N")
                messages.success(self.request, f"Éxito al registrar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al registrar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)

class SaleUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'change_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        detail_sale =list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
             "product","product__description","quantity","price","subtotal","iva"))
        print("detalle")
        detail_sale=json.dumps(detail_sale,default=custom_serializer)
        context['detail_sales']=detail_sale  #[{'id':1,'precio':2},{},{}]
        context['save_url'] = reverse_lazy('sales:sales_update',kwargs={"pk":self.object.id})
        print(detail_sale)
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request update")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al actualizar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            print("facturaId: ")
            print(self.kwargs.get('pk'))
            sale= Invoice.objects.get(id=self.kwargs.get('pk'))
           
            with transaction.atomic():
                sale.customer_id=int(data['customer'])
                sale.payment_method_id=int(data['payment_method'])
                sale.issue_date=data['issue_date']
                sale.subtotal=Decimal(data['subtotal'])
                sale.discount=Decimal(data['discount'])
                sale.iva= Decimal(data['iva'])
                sale.total=Decimal(data['total'])
                sale.payment=Decimal(data['payment'])
                sale.change=Decimal(data['change'])
                sale.state='M'
                sale.save()
                details = json.loads(request.POST['detail'])
                print(details)
                detdelete=InvoiceDetail.objects.filter(invoice_id=sale.id)
                for det in detdelete:
                    det.product.stock+= int(det.quantity)
                    det.product.save()
                detdelete.delete()
               
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "M")
                messages.success(self.request, f"Éxito al Modificar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al Modificar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)

class SaleCancelView(PermissionMixin, View):
    permission_required = 'delete_invoice'
    
    def post(self, request, *args, **kwargs):
        try:
            sale = Invoice.objects.get(id=self.kwargs.get('pk'))
            if sale.state == 'A':
                messages.error(self.request, "LA VENTA YA ESTÁ ANULADA")
                return redirect('sales:sales_list') 

            current_time = timezone.now()
            time_difference = current_time - sale.issue_date
            if time_difference > timedelta(days=3):
                messages.error(self.request, "La venta ya no puede ser anulada, pasaron los dias establecidos")
                return redirect('sales:sales_list') 
            
            
            with transaction.atomic():
                sale.state = 'A'  # Estado de "Anulado"
                sale.save()
                
                details = InvoiceDetail.objects.filter(invoice_id=sale.id)
                for detail in details:
                    product = detail.product
                    product.stock += detail.quantity
                    product.save()
                    
                save_audit(request, sale, "A")
                messages.success(self.request, f"Éxito al anular la venta F#{sale.id}")
                return redirect('sales:sales_list') 
        except Invoice.DoesNotExist:
            messages.error(self.request, "Factura No encontrada")
            return redirect('sales:sales_list') 
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)
        
class SaleDeleteView(PermissionMixin, View):
    permission_required = 'delete_invoice'
    
    def post(self, request, *args, **kwargs):
        try:
            sale = Invoice.objects.get(id=self.kwargs.get('pk'))
            current_time = timezone.now()
            
            if sale.active == False:
                messages.error(self.request, f"Error al eliminar la venta")
                return redirect('sales:sales_list') 
            
            if sale.issue_date.date() != current_time.date():
                messages.error(self.request, f"Error al eliminar la venta")
                return redirect('sales:sales_list') 
            
            with transaction.atomic():
                sale.active = False  # Estado de "Cancelado"
                sale.save()
                
                details = InvoiceDetail.objects.filter(invoice_id=sale.id)
                for detail in details:
                    product = detail.product
                    product.stock += detail.quantity
                    product.save()
                    
                save_audit(request, sale, "False")
                messages.success(request, f"Éxito al eliminar la venta F#{sale.id}")
                return redirect('sales:sales_list') 
        except Invoice.DoesNotExist:
            
            return redirect('sales:sales_list') 
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)

class SalesConsultView(TemplateView):
    template_name = 'sales/invoices/consult.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_id = self.kwargs.get('pk')  # Obtén el pk de la URL
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        company = Company.objects.filter(id=1)
        print(company)
        context['company'] = company
        context['invoice'] = invoice
        return context


def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    company = Company.objects.filter(id=1)

    template = get_template('sales/invoices/pdfgenera.html')
    context = {
        'invoice': invoice,
        'company': company,
    }
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"invoice_{invoice_id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response

    return HttpResponse("Error generando el PDF", status=400)