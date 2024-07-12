from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from app.security.models import GroupModulePermission
from app.security.mixins.mixins import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from app.core.forms.group_module_permissions import GroupModulePermissionForm
from django.contrib import messages

class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/group_module_permission/list.html'
    model = GroupModulePermission
    context_object_name = 'group_module_permissions'
    permission_required = 'view_groupmodulepermission'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1:
            query.add(Q(group__name__icontains=q1), Q.OR)
            query.add(Q(module__name__icontains=q1), Q.OR)
            query.add(Q(permissions__name__icontains=q1), Q.OR)
        return self.model.objects.filter(query).distinct().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:group_module_permission_add')
        return context


class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    form_class = GroupModulePermissionForm
    template_name = 'security/group_module_permission/form.html'
    permission_required = 'add_groupmodulepermission'
    success_url = reverse_lazy('core:group_module_permission_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grupo-Modulo-Permisos'
        context['grabar'] = 'Grabar Grupo-Modulo-Permisos'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group_module_permission = self.object
        messages.success(self.request, f"Éxito al crear.")
        return response


class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/group_module_permission/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('core:group_module_permission_list')
    permission_required = 'change_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grupo Módulo Permiso'
        context['grabar'] = 'Actualizar Grupo Módulo Permiso'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group_module_permission = self.object
        messages.success(self.request, f"Éxito al actualizar el grupo módulo permiso {group_module_permission.module.name} - {group_module_permission.group.name}.")
        return response

class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:group_module_permission_list')
    permission_required = 'delete_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Grupo-Modulo-Permisos'
        context['name'] = f"¿Desea Eliminar el Grupo-Modulo: {self.object.module.name}?"
        context['back_url'] = self.success_url
        return context







