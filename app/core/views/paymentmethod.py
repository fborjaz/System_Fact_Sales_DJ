from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import PaymentMethodForm
from app.core.models import PaymentMethod
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q


class PaymentMethodListView(ListViewMixin, ListView):
    template_name = 'core/paymentmethod/list.html'
    model = PaymentMethod
    context_object_name = "paymentmethods"
    permission_required = "view_paymentmethod"
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_paymentmethod', '')
        context['create_url'] = reverse_lazy('core:paymentmethod_create')
        return context
    
class PaymentMethodCreateView(CreateViewMixin, CreateView):
    model = PaymentMethod
    template_name = 'core/paymentmethod/form.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('core:paymentmethod_list')
    permission_required = 'add_paymentmethod'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['grabar'] = 'Grabar Metodo de Pago'
        context['back_url'] = self.success_url
        return context

class PaymentMethodUpdateView(UpdateViewMixin, UpdateView):
    model = PaymentMethod
    template_name = 'core/paymentmethod/form.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('core:paymentmethod_list')
    permission_required = 'change_paymentmethod'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Metodo de Pago'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        paymentmethod = self.object
        messages.success(self.request, f"Éxito al actualizar el Metodo de Pago {paymentmethod.description}.")
        return response

class PaymentMethodDeleteView(PermissionMixin, DeleteView):
    model = PaymentMethod
    template_name = 'core/paymentmethod/delete.html'
    success_url = reverse_lazy('core:paymentmethod_list')
    permission_required = 'delete_paymentmethod'
    
    def delete(self, request, *args, **kwargs):
        paymentmethod = self.get_object()
        paymentmethod.active = False
        paymentmethod.save()
        messages.success(request, f"Metodo de Pago {paymentmethod.description} eliminado con éxito.")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        return context