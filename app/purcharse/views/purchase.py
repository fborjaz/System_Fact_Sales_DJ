import json
from decimal import Decimal
from datetime import timedelta
import logging

from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, View, TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from io import BytesIO

from app.core.models import Product, Supplier
from app.purcharse.forms import PurchaseForm
from app.purcharse.models import Purchase, PurchaseDetail
from app.security.mixins.mixins import PermissionMixin, CreateViewMixin, UpdateViewMixin, ListViewMixin
from proy_sales.utils import custom_serializer, save_audit

logger = logging.getLogger(__name__)

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchase/list.html'
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'
    paginate_by = 5

    def get_queryset(self):
        queryset = self.model.objects.order_by('-issue_date')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(id=q) | Q(supplier__name__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        purchases = paginator.get_page(page)

        context['purchases'] = purchases
        context['title1'] = 'IC - Compras'
        context['title2'] = 'Consulta de las Compras'
        context['create_url'] = reverse_lazy('purchase:purchase_create')
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
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        context['detail_purchases'] = []
        context['title1'] = 'IC - Compras'
        context['title2'] = 'Crear una nueva compra'
        context['save_url'] = reverse_lazy('purcharse:purchase_create')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(self.request, f"Error al registrar la compra: {form.errors}.")
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
                    product = Product.objects.get(id=int(detail['id']))
                    product.stock += Decimal(detail['quantify'])
                    product.save()
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product=product,
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                save_audit(request, purchase, "A")
                messages.success(self.request, f"Éxito al registrar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al registrar la compra"}, status=200)
        except IntegrityError:
            messages.error(self.request, "Error: Ya existe una compra con este número de documento.")
            return JsonResponse({"msg": "Error: Ya existe una compra con este número de documento."}, status=400)
        except Exception as ex:
            logger.exception(ex) 
            messages.error(self.request, "Error inesperado al procesar la compra.")
            return JsonResponse({"msg": "Error inesperado al procesar la compra."}, status=500)

class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'purchase/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase:purchase_list')
    permission_required = 'change_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        detail_purchase = list(PurchaseDetail.objects.filter(purchase_id=self.object.id).values(
            "product", "product__description", "quantify", "cost", "subtotal", "iva"))
        detail_purchase = json.dumps(detail_purchase, default=custom_serializer)
        context['detail_purchases'] = detail_purchase
        context['title1'] = 'IC - Compras'
        context['title2'] = 'Actualiza tus Compras'
        context['save_url'] = reverse_lazy('purcharse:purchase_update', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(self.request, f"Error al actualizar la compra: {form.errors}.")
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

                # Restablecer el stock de productos a su estado anterior
                detdelete = PurchaseDetail.objects.filter(purchase_id=purchase.id)
                for det in detdelete:
                    det.product.stock -= int(det.quantify)
                    det.product.save()
                detdelete.delete()

                details = json.loads(request.POST['detail'])
                for detail in details:
                    product = Product.objects.get(id=int(detail['id']))
                    product.stock += Decimal(detail['quantify'])
                    product.save()
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product=product,
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                save_audit(request, purchase, "M")
                messages.success(self.request, f"Éxito al modificar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al modificar la compra"}, status=200)
        except IntegrityError:
            messages.error(self.request, "Error: Ya existe una compra con este número de documento.")
            return JsonResponse({"msg": "Error: Ya existe una compra con este número de documento."}, status=400)
        except Exception as ex:
            logger.exception(ex) 
            messages.error(self.request, "Error inesperado al procesar la compra.")
            return JsonResponse({"msg": "Error inesperado al procesar la compra."}, status=500)

class PurchaseCancelView(PermissionMixin, View):
    permission_required = 'delete_purchase'

    def post(self, request, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))

            if purchase.state == 'A':
                messages.error(self.request, "La compra ya está anulada.")
                return redirect('purchase:purchase_list')

            current_time = timezone.now()
            time_difference = current_time - purchase.issue_date
            if time_difference <= timedelta(days=3):
                with transaction.atomic():
                    purchase.state = 'A'
                    purchase.save()

                    # Revertir el stock de los productos
                    for detail in purchase.details:
                        product = detail.product
                        product.stock += detail.quantify
                        product.save()

                    save_audit(request, purchase, "A")  # Registrar la anulación en la auditoría
                    messages.success(self.request, f"Éxito al anular la compra C#{purchase.id}")
            else:
                messages.error(request, "La compra no puede ser anulada. Han pasado más de 3 días desde su emisión.")

        except Purchase.DoesNotExist:
            messages.error(request, "Compra no encontrada.")
        except Exception as ex:
            logger.exception(ex)  # Registrar la excepción con detalles
            messages.error(request, f"Error inesperado al anular la compra.")

        return redirect('purchase:purchase_list')


class PurchaseDeleteView(PermissionMixin, View):
    permission_required = 'delete_purchase'

    def post(self, request, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))

            with transaction.atomic():
                PurchaseDetail.objects.filter(purchase=purchase).delete()
                purchase.delete()
                save_audit(request, purchase, "D")
                messages.success(request, f"Éxito al eliminar la compra C# {purchase.id}")

        except Purchase.DoesNotExist:
            messages.error(request, "Compra no encontrada.")
        except Exception as ex:
            logger.exception(ex)
            messages.error(request, f"Error inesperado al eliminar la compra.")

        return redirect('purchase:purchase_list')

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
    template = get_template('purchase/pdfgenera.html')
    context = {'purchase': purchase,}
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"purchase_{purchase_id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generando el PDF", status=400)