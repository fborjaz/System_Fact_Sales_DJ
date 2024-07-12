from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic import TemplateView
from app.security.models import Menu
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from app.core.forms.menu import MenuForm

#Presentar todos los modulos
class MenuListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/menu/list.html'
    model = Menu
    context_object_name = 'menus'  
    permission_required = 'view_menu'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class MenuCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Menu
    template_name = 'security/menu/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('core:menus_list')
    permission_required = 'add_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Módulo'
        context['grabar'] = 'Grabar Menu'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Éxito al crear el menu {menu.name}.")
        return response


class MenuUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Menu
    template_name = 'security/menu/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('core:menus_list')
    permission_required = 'change_menu'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'Módulo'
       context['grabar'] = 'Actualizar Menú'
       context['back_url'] = self.success_url
       return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Éxito al actualizar el menu {menu.name}.")
        return response

class MenuDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Menu
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:menus_list')
    permission_required = 'delete_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Menu'
        context['name'] = f"¿Desea Eliminar el menu: {self.object.name}?"
        context['back_url'] = self.success_url
        return context


