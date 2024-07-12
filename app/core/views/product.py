from django.urls import reverse_lazy
from app.core.forms.product import ProductForm
from app.core.models import Product
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProductListView(PermissionMixin, ListViewMixin, ListView):
  model = Product
  template_name = 'core/products/list.html'
  context_object_name = 'products'
  permission_required = 'view_product'
  paginate_by = 4

  def get_queryset(self):
    q = self.request.GET.get('q')
    queryset = self.model.objects.all().order_by('id')

    if q:
      try:
        # Intenta buscar por ID primero
        product_id = int(q)
        queryset = queryset.filter(id=product_id)
      except ValueError:
        # Si no es un número, busca por descripción
        queryset = queryset.filter(description__icontains=q)

    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    queryset = self.get_queryset()
    paginator = Paginator(queryset, self.paginate_by)

    page = self.request.GET.get('page')
    try:
      products = paginator.page(page)
    except PageNotAnInteger:
      products = paginator.page(1)
    except EmptyPage:
      products = paginator.page(paginator.num_pages)

    context['brands'] = products
    context['title1'] = 'Productos'
    context['title2'] = 'Consulta de Productos'
    context['create_url'] = reverse_lazy('core:product_create')
    context['query'] = self.request.GET.get('q', '')
    return context


class ProductCreateView(PermissionMixin, CreateViewMixin, CreateView):
  model = Product
  form_class = ProductForm
  template_name = 'core/products/form.html'
  success_url = reverse_lazy('core:product_list')
  permission_required = 'add_product'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title1'] = 'Crear Producto'
    context['title2'] = 'Producto'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    product = self.object
    messages.success(self.request, f"Éxito al crear el producto {product.description}.")
    return response


class ProductUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
  model = Product
  form_class = ProductForm
  template_name = 'core/products/form.html'
  success_url = reverse_lazy('core:product_list')
  permission_required = 'change_product'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title1'] = 'Actualizar Producto'
    context['title2'] = 'Actualizar Datos Del Producto'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    product = self.object
    messages.success(self.request, f"Éxito al actualizar el producto {product.description}.")
    return response


# class ProductDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
#   model = Product
#   template_name = 'core/delete.html'
#   success_url = reverse_lazy('core:product_list')
#   permission_required = 'delete_product'
#
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.object = None
#
#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'Eliminar Producto'
#     context['description'] = f"¿Desea eliminar el producto: {self.object.description}?"
#     context['back_url'] = self.success_url
#     return context
#
#   def delete(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     success_message = f"Éxito al eliminar el producto {self.object.description}."
#     self.object.delete()
#     messages.success(self.request, success_message)
#     return super().delete(request, *args, **kwargs)

class ProductDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Product
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:product_list')
    permission_required = 'delete_product'

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.object = None

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Eliminar Producto'
      context['description'] = f"¿Desea eliminar el producto: {self.object.description}?"
      context['back_url'] = self.success_url
      return context

    def delete(self, request, *args, **kwargs):
      self.object = self.get_object()
      success_message = f"Éxito al eliminar el producto {self.object.description}."

      # Marcar el producto como inactivo en lugar de eliminarlo
      self.object.active = False
      self.object.save()

      messages.success(self.request, success_message)
      return super().delete(request, *args, **kwargs)
