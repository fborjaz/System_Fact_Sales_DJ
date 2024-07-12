from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Supplier
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SupplierListView(PermissionMixin, ListViewMixin, ListView):
  model = Supplier
  template_name = 'core/suppliers/list.html'
  context_object_name = 'suppliers'
  permission_required = 'view_supplier'
  paginate_by = 4

  def get_queryset(self):
    q1 = self.request.GET.get('q')
    if q1:
      query = Q(ruc__icontains=q1)
    else:
      query = Q(active=True)

    return self.model.objects.filter(query).order_by('id')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    queryset = self.get_queryset()
    paginator = Paginator(queryset, self.paginate_by)

    page = self.request.GET.get('page')
    try:
      suppliers = paginator.page(page)
    except PageNotAnInteger:
      suppliers = paginator.page(1)
    except EmptyPage:
      suppliers = paginator.page(paginator.num_pages)

    context['suppliers'] = suppliers
    context['create_url'] = reverse_lazy('core:supplier_create')
    context['query'] = self.request.GET.get('q', '')
    return context


class SupplierCreateView(PermissionMixin, CreateViewMixin, CreateView):
  model = Supplier
  form_class = SupplierForm
  template_name = 'core/suppliers/form.html'
  success_url = reverse_lazy('core:supplier_list')
  permission_required = 'add_supplier'

  def get_context_data(self, **kwargs):
    context = super().get_context_data()
    context['title1'] = 'Crear Proveedor'
    context['title2'] = 'Proveedor'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    supplier = self.object
    messages.success(self.request, f"Éxito al crear al proveedor {supplier.name}.")
    return response


class SupplierUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
  model = Supplier
  form_class = SupplierForm
  template_name = 'core/suppliers/form.html'
  success_url = reverse_lazy('core:supplier_list')
  permission_required = 'change_supplier'

  def get_context_data(self, **kwargs):
    context = super().get_context_data()
    context['title1'] = 'Actualizar Proveedor '
    context['title2'] = 'Actualizar Datos del Proveedor '
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    supplier = self.object
    messages.success(self.request, f"Éxito al actualizar el proveedor {supplier.name}.")
    return response


class SupplierDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
  model = Supplier
  template_name = 'core/delete.html'
  success_url = reverse_lazy('core:supplier_list')
  permission_required = 'delete_supplier'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.object = None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['grabar'] = 'Eliminar Proveedor'
    context['description'] = f"¿Desea eliminar al proveedor: {self.object.name}?"
    context['back_url'] = self.success_url
    return context

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    success_message = f"Éxito al eliminar lógicamente la marca {self.object.description}."
    self.object.delete()
    messages.success(self.request, success_message)
    return super().delete(request, *args, **kwargs)
