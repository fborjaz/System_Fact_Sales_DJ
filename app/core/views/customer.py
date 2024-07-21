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
    model = Customer
    template_name = 'core/customer/list.html'
    context_object_name = 'customers'
    permission_required = "view_customer"
    paginate_by = 4

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")

        order_by = self.request.GET.get('o', 'id')
        return self.model.objects.filter(self.query).order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            customers = paginator.page(page)
        except PageNotAnInteger:
            customers = paginator.page(1)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)

        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_customer', '')
        context['customers'] =  customers
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

    def form_valid(self, form):
        response = super().form_valid(form)
        customers = self.object
        messages.success(self.request, f"Éxito al crear el cliente {customers.first_name}.")
        return response

class CustomerUpdateView(UpdateViewMixin, UpdateView):
    model = Customer
    template_name = 'core/customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'change_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Actualizar Cliente'
        context['title2'] = 'Cliente'
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
