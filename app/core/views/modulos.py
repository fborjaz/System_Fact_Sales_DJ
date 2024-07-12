from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic import TemplateView
from app.security.models import Module
from django.urls import reverse_lazy
from django.db.models import Q
from app.core.forms.modules import ModuleForm
from django.contrib import messages

class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'components/modulos.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"]= "IC - Modulos"
        context["title2"]= "Modulos Disponibles"
        MenuModule(self.request).fill(context)
        print(context)
        return context
    
#Presentar todos los modulos
class ModulesListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/modulos/list.html'
    model = Module
    context_object_name = 'modules'
    permission_required = 'view_module'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:supplier_create')
        return context


class ModuleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Module
    template_name = 'security/modulos/form.html'
    form_class = ModuleForm
    success_url = reverse_lazy('core:modules_list')
    permission_required = 'add_module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Módulo'
        context['grabar'] = 'Grabar Módulo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(self.request, f"Éxito al crear el módulo {module.name}.")
        return response

class ModuleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Module
    template_name = 'security/modulos/form.html'
    form_class = ModuleForm
    success_url = reverse_lazy('core:modules_list')
    permission_required = 'change_module'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'Módulo'
       context['grabar'] = 'Actualizar Módulo'
       context['back_url'] = self.success_url
       return context

    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(self.request, f"Éxito al actualizar el módulo {module.name}.")
        return response

class ModuleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Module
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:modules_list')
    permission_required = 'delete_module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Modulo'
        context['name'] = f"¿Desea Eliminar el modulo: {self.object.name}?"
        context['back_url'] = self.success_url
        return context



