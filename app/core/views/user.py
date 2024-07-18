from django.views.generic import ListView
from django.contrib.auth.models import User
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.models import User
from app.core.forms.user import UserGroupForm

User = get_user_model()

class UsersListView(PermissionRequiredMixin, ListView):
    template_name = 'security/usuarios/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'auth.view_user'  # Ensure the correct permission

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('groups').filter(is_superuser=False)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(username__icontains=q)
        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:modules_create')  # Replace with your create URL
        return context


class UserGroupView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserGroupForm(instance=user)
        return render(request, 'security/usuarios/form.html', {'form': form, 'title': 'Asignar/Quitar Grupos'})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserGroupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:users_list')
        return render(request, 'security/usuarios/form.html', {'form': form, 'title': 'Asignar/Quitar Grupos'})


class UserDeleteView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('core:users_list')






