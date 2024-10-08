from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from app.core.forms.supplier import CompanyForm
from app.core.models import Company
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CompanyListView(ListViewMixin, ListView):
    model = Company
    template_name = 'core/company/list.html'
    context_object_name = "companies"
    permission_required = "view_company"
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            company = paginator.page(page)
        except PageNotAnInteger:
            company = paginator.page(1)
        except EmptyPage:
            company = paginator.page(paginator.num_pages)

        context['companys'] = company
        context['title1'] = 'IC - Compañia'
        context['title2'] = 'Consulta de Compañias'
        context['create_url'] = reverse_lazy('core:company_create')
        context['query'] = self.request.GET.get('q', '')
        return context


class CompanyCreateView(CreateViewMixin, CreateView):
    model = Company
    template_name = 'core/company/form.html'
    form_class = CompanyForm
    success_url = reverse_lazy("core:company_list")
    permission_required = 'add_company'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Crear Compañia'
        context['title2'] = 'Compañia'
        context['back_url'] = self.success_url
        return context
    
class CompanyUpdateView(UpdateViewMixin, UpdateView):
    model = Company
    template_name = 'core/company/form.html'
    form_class = CompanyForm
    success_url = reverse_lazy('core:company_list')
    permission_required = 'change_company'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Actualizar Compañia'
        context['title2'] = 'Compañia'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        company = self.object
        messages.success(self.request, f"Éxito al actualizar la Empresa {company.name}.")
        return response

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'core/company/delete.html'
    success_url = reverse_lazy('core:company_list')
    permission_required = 'delete_company'
    
    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        company.active = False
        company.save()
        messages.success(request, f"Éxito al eliminar la Empresa {company.name}.")
        return super().delete(request, *args, **kwargs)
        