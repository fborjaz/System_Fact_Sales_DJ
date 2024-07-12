from django.urls import reverse_lazy
from app.core.forms.category import CategoryForm
from app.core.models import Category
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CategoryListView(PermissionMixin, ListViewMixin, ListView):
  model = Category
  template_name = 'core/categories/list.html'
  context_object_name = 'Category'
  permission_required = 'view_category'
  paginate_by = 4

  def get_queryset(self):
    q1 = self.request.GET.get('q')
    if q1:
      query = Q(description__icontains=q1)
    else:
      query = Q(active=True)

    return self.model.objects.filter(query).order_by('id')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    queryset = self.get_queryset()
    paginator = Paginator(queryset, self.paginate_by)

    page = self.request.GET.get('page')
    try:
      categories = paginator.page(page)
    except PageNotAnInteger:
      categories = paginator.page(1)
    except EmptyPage:
      categories = paginator.page(paginator.num_pages)

    context['categories'] = categories
    context['title1'] = 'Categorias'
    context['title2'] = 'Consulta de Categorias'
    context['create_url'] = reverse_lazy('core:category_create')
    context['query'] = self.request.GET.get('q', '')
    return context


class CategoryCreateView(PermissionMixin, CreateViewMixin, CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'core/categories/form.html'
  success_url = reverse_lazy('core:category_list')
  permission_required = 'add_category'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title1'] = 'Crear Categoria'
    context['title2'] = 'Categoria'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    category = self.object
    messages.success(self.request, f"Éxito al crear la categoría {category.description}.")
    return response


class CategoryUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
  model = Category
  form_class = CategoryForm
  template_name = 'core/categories/form.html'
  success_url = reverse_lazy('core:category_list')
  permission_required = 'change_category'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title1'] = 'Actualizar Categoría'
    context['title2'] = 'Actualizar Datos De Categoría'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    response = super().form_valid(form)
    category = self.object
    messages.success(self.request, f"Éxito al actualizar la categoría {category.description}.")
    return response


class CategoryDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
  model = Category
  template_name = 'core/delete.html'
  success_url = reverse_lazy('core:category_list')
  permission_required = 'delete_category'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.object = None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Eliminar Marca'
    context['description'] = f"¿Desea eliminar la marca: {self.object.description}?"
    context['back_url'] = self.success_url
    return context

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    success_message = f"Éxito al eliminar la categoría {self.object.description}."
    self.object.delete()
    messages.success(self.request, success_message)
    return super().delete(request, *args, **kwargs)
