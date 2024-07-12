from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import IvaForm
from app.core.models import Iva
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# -- IVA CLASS -- #
class IvaListView(ListViewMixin, ListView):
    template_name = 'core/iva/list.html'
    model = Iva
    context_object_name = "ivas"
    permission_required = "view_iva"
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        print()
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_iva', '')
        context['create_url'] = reverse_lazy('core:iva_create')
        return context

class IvaCreateView(CreateViewMixin, CreateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'add_iva'
    print(form_class)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Iva'
        context['back_url'] = self.success_url
        return context

class IvaUpdateView(UpdateViewMixin, UpdateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'change_iva'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Iva'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        iva = self.object
        messages.success(self.request, f"Éxito al actualizar la Categoria {iva.description}.")
        return response

class IvaDeleteView(PermissionMixin, DeleteView):
    model = Iva
    template_name = 'core/iva/delete.html'
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'delete_iva'
    
    def delete(self, request, *args, **kwargs):
        iva = self.get_object()
        iva.active = False
        iva.save()
        messages.success(request, f"Éxito al eliminar la Categoria {iva.description}.")
        return super().delete(request, *args, **kwargs)