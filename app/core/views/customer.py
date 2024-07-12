from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import CustomerForm 
from app.core.models import Customer
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# -- CLASS CUSTOMER --#
class CustomerListView(ListViewMixin, ListView):
    template_name = 'core/customer/list.html'
    model = Customer
    permission_required = "view_customer"

    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(first_name__icontains=q1) | Q(last_name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)

        context['customers'] = customer
        context['title1'] = 'IC - Clientes'
        context['title2'] = 'Consulta de Clientes'
        context['create_url'] = reverse_lazy('core:customer_create')
        context['query'] = self.request.GET.get('q', '')
        return context

class CustomerCreateView(CreateViewMixin, CreateView):
    model = Customer
    template_name = 'core/customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'add_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Crear Cliente'
        context['title2'] = 'Cliente'
        context['back_url'] = self.success_url
        return context

class CustomerUpdateView(UpdateViewMixin, UpdateView):
    model = Customer
    template_name = 'core/customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'change_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'IC - Actualizar Cliente'
        context['back_url'] = self.success_url
        return context

class CustomerDeleteView(PermissionMixin, DeleteView):
    model = Customer
    template_name = 'core/customer/delete.html'
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'delete_customer'

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        messages.success(request, f"Cliente {customer.first_name} eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        return context
