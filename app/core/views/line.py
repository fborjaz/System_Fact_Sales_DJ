from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import LineForm 
from app.core.models import Line
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# -- LINE CLASS --#
class LineListView(ListViewMixin, ListView):
    template_name = 'core/lines/list.html'
    model = Line
    context_object_name = "lines"
    permission_required = "view_line"
    
    def get_queryset(self):
        self.query = Q(active=True)
        q1 = self.request.GET.get('q')
        print()
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            line = paginator.page(page)
        except PageNotAnInteger:
            line = paginator.page(1)
        except EmptyPage:
            line = paginator.page(paginator.num_pages)

        context['lines'] = line
        context['title1'] = 'IC - Lineas'
        context['title2'] = 'Consulta de lineas'
        context['create_url'] = reverse_lazy('core:line_create')
        context['query'] = self.request.GET.get('q', '')
        return context

    

class LineCreateView(CreateViewMixin, CreateView):
    model = Line
    template_name = 'core/lines/form.html'
    form_class = LineForm
    success_url = reverse_lazy('core:line_list')
    permission_required = 'add_line'
    #print(form_class)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Registrar una línea'
        context['title2'] = 'Línea'
        context['back_url'] = self.success_url
        return context

class LineUpdateView(UpdateViewMixin, UpdateView):
    model = Line
    template_name = 'core/lines/form.html'
    form_class = LineForm
    success_url = reverse_lazy('core:line_list')
    permission_required = 'change_line'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Actualizar una línea'
        context['title2'] = 'Línea'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        brand = self.object
        messages.success(self.request, f"Éxito al actualizar la linea {brand.description}.")
        return response

class LineDeleteView(PermissionMixin, DeleteView):
    model = Line
    template_name = 'core/lines/delete.html'
    success_url = reverse_lazy('core:line_list')
    permission_required = 'delete_line'
    
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.active = False
        object.save()
        messages.success(request, f"Linea {object.description} eliminada con éxito.")
        return super().delete(request, *args, **kwargs)
    
    