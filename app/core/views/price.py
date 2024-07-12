from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import ProductPriceForm
from app.core.models import ProductPrice
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q


# -- Price Product CLASS -- #
class ProductPriceListView(ListViewMixin, ListView):
    template_name = 'core/price/list.html'
    model = ProductPrice
    context_object_name = "precios"
    permission_required = "view_productprice"
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        print()
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_productprice', '')
        context['create_url'] = reverse_lazy('core:price_create')
        return context

class ProductPriceCreateView(CreateViewMixin, CreateView):
    model = ProductPrice
    template_name = 'core/price/form.html'
    form_class = ProductPriceForm
    success_url = reverse_lazy('core:price_list')
    permission_required = 'add_productprice'
    print(form_class)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Precio'
        context['back_url'] = self.success_url
        return context
    
class ProductPriceUpdateView(UpdateViewMixin, UpdateView):
    model = ProductPrice
    template_name = 'core/price/form.html'
    form_class = ProductPriceForm
    success_url = reverse_lazy('core:price_list')
    permission_required = 'change_productprice'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Precio'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        price = self.object
        messages.success(self.request, f"Éxito al actualizar la Categoria {price.category}.")
        return response

class ProductPriceDeleteView(PermissionMixin, DeleteView):
    model = ProductPrice
    template_name = 'core/price/delete.html'
    success_url = reverse_lazy('core:price_list')
    permission_required = 'delete_productprice'
    
    def delete(self, request, *args, **kwargs):
        price = self.get_object()
        price.active = False
        price.save()
        messages.success(request, f"Éxito al eliminar el Precio {price.description}.")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        return context

