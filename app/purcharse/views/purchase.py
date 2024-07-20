from io import BytesIO
import json
from urllib import request
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View, TemplateView
from django.contrib import messages
from django.db.models import Q, F
from decimal import Decimal
from datetime import timedelta
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import get_template
from xhtml2pdf import pisa
from app.core.models import Product, Supplier
from app.purcharse.forms import PurchaseForm
from app.purcharse.models import Purchase, PurchaseDetail
from app.security.mixins.mixins import PermissionMixin, CreateViewMixin, UpdateViewMixin, ListViewMixin
from proy_sales.utils import custom_serializer, save_audit

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchase/list.html'
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        if q1 is not None: 
            self.query.add(Q(id=q1), Q.OR)
            self.query.add(Q(supplier__name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            purchases = paginator.page(page)
        except PageNotAnInteger:
            purchases = paginator.page(1)
        except EmptyPage:
            purchases = paginator.page(paginator.num_pages)

        context['purchases'] = purchases
        context['title1'] = 'IC - Compras'
        context['title2'] = 'Consulta de las Compras'
        context['create_url'] = reverse_lazy('purcharse:purchase_create')
        context['query'] = self.request.GET.get('q', '')
        return context


class PurchaseCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Purchase
    template_name = 'purchase/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase:purchase_list')
    permission_required = 'add_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'cost', 'stock', 'iva__value')
        context['detail_purchases'] = []
        context['title1'] = 'IC - Crear Compra'
        context['title2'] = 'Compras'
        context['save_url'] = reverse_lazy('purcharse:purchase_create')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        purchase = self.object
        messages.success(self.request, f"Éxito al crear al proveedor {purchase.name}.")
        return response
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.success(self.request, f"Error al registrar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        data = request.POST
        try:
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    supplier_id=int(data['supplier']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    iva=Decimal(data['iva']),
                    total=Decimal(data['total'])
                )
                details = json.loads(request.POST['detail'])
                for detail in details:
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product_id=int(detail['id']),
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['cost']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                save_audit(request, purchase, "A")
                messages.success(self.request, f"Éxito al registrar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al registrar la compra"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)

class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'purchase/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase:purchase_list')
    permission_required = 'change_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'cost', 'stock', 'iva__value')
        detail_purchase = list(PurchaseDetail.objects.filter(purchase_id=self.object.id).values(
            "product", "product__description", "quantify", "cost", "subtotal", "iva"))
        detail_purchase = json.dumps(detail_purchase, default=custom_serializer)
        context['detail_purchases'] = detail_purchase
        context['save_url'] = reverse_lazy('purchase:purchase_update', kwargs={"pk": self.object.id})
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.success(self.request, f"Error al actualizar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        data = request.POST
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))
            with transaction.atomic():
                purchase.num_document = data["num_document"]
                purchase.supplier_id = int(data['supplier'])
                purchase.issue_date = data['issue_date']
                purchase.subtotal = Decimal(data['subtotal'])
                purchase.iva = Decimal(data['iva'])
                purchase.total = Decimal(data['total'])
                purchase.save()
                detdelete = PurchaseDetail.objects.filter(purchase_id=purchase.id)
                for det in detdelete:
                    det.product.stock += int(det.quantify)
                    det.product.save()
                detdelete.delete()
                details = json.loads(request.POST['detail'])
                for detail in details:
                    Pur_detail = PurchaseDetail.objects.create(
                        purchase=purchase,
                        product_id=int(detail['id']),
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['cost']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    ) 
                    Pur_detail.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, purchase, "M")
                messages.success(self.request, f"Éxito al modificar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al modificar la compra"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)


class PurchaseDeleteView(PermissionMixin, View):
    permission_required = 'delete_purchase'
    
    def post(self, request, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))
            if not self._can_delete_purchase(purchase):
                messages.error(self.request, "Error al eliminar la compra. Condiciones no cumplidas.")
                return redirect('purchase:purchase_list')
            with transaction.atomic():
                self._revert_stock_and_delete(purchase)
                messages.success(request, f"Éxito al eliminar la compra N#{purchase.id}")
        except Purchase.DoesNotExist:
            messages.error(self.request, "La compra no existe.")
        except Exception as ex:
            messages.error(self.request, f"Error inesperado: {ex}")
        return redirect('purchase:purchase_list')

    def _can_delete_purchase(self, purchase):
        current_time = timezone.now()
        return purchase.active and purchase.issue_date.date() == current_time.date()

    def _revert_stock_and_delete(self, purchase):
        for detail in purchase.purchasedetail_set.all():
            detail.product.stock += detail.quantify
            detail.product.save()
        purchase.delete()  
        save_audit(request, purchase, "False")

class PurchaseConsultView(TemplateView):
    template_name = 'purchase/consult.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_id = self.kwargs.get('pk')
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        context['purchase'] = purchase
        return context

def generate_purchase_pdf(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    template = get_template('purchase/pdfgenerate.html')
    context = {
        'purchase': purchase,
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"purchase_{purchase_id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generando el PDF", status=400)
