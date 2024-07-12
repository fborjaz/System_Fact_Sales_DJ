from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.contrib import messages
from app.core.forms.forms import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash


# # PAGINATION
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProfileView(View):
  def get(self, request):
    data = {
      "title1": "IC - Perfil",
      "title2": "Perfil de Usuario"
    }
    return render(request, 'core/profile.html', data)


class UpdateProfileView(View):
  def get(self, request):
    data = {
      "title1": "IC - Actualizar Perfil",
      "title2": "Actualizar Perfil"
    }
    form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'core/update_profile.html', {'form': form, **data})

  def post(self, request):
    data = {
      "title1": "IC - Actualizar Perfil",
      "title2": "Actualizar Perfil"
    }
    form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
      return redirect('security:auth_profile')
    return render(request, 'core/update_profile.html', {'form': form, **data})


class SignupView(View):
  def get(self, request):
    data = {
      "title1": "IC - Registro",
      "title2": "Registro de Administradores"
    }
    form = CustomUserCreationForm()
    return render(request, "security/auth/signup.html", {"form": form, **data})

  def post(self, request):
    data = {
      "title1": "IC - Registro",
      "title2": "Registro de Usuarios"
    }
    form = CustomUserCreationForm(request.POST, request.FILES)
    if form.is_valid():
      user = form.save()
      messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
      return redirect("security:auth_login")
    else:
      error_messages = []
      for field in form:
        for error in field.errors:
          error_messages.append(f"{field.label}: {error}")
      for error in form.non_field_errors():
        error_messages.append(error)
      data["errors"] = error_messages
      return render(request, "security/auth/signup.html", {"form": form, **data})


class SigninView(LoginView):
  template_name = 'security/auth/signin.html'
  success_url = reverse_lazy('modulos')
  redirect_authenticated_user = True
  form_class = AuthenticationForm
  extra_context = {
    "title1": "Login",
    "title2": "Inicio de Sesión"
  }

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["success_messages"] = messages.get_messages(self.request)
    return context

  def form_valid(self, form):
    user = authenticate(self.request, username=form.cleaned_data.get('username'),
                        password=form.cleaned_data.get('password'))
    if user is not None:
      login(self.request, user)
      return redirect(self.success_url)
    else:
      return self.render_to_response(self.get_context_data(
        form=form,
        error="El usuario o la contraseña son incorrectos"
      ))

  def form_invalid(self, form):
    return self.render_to_response(self.get_context_data(
      form=form,
      error="Datos inválidos"
    ))


class SignoutView(LogoutView):
  next_page = 'home'


class ChangePasswordView(PasswordChangeView):
  form_class = CustomPasswordChangeForm
  template_name = 'core/reseteo.html'
  success_url = '/modulos'

  def get_context_data(self, **kwargs):
    data = super().get_context_data(**kwargs)
    data['title1'] = "IC - Cambiar Contraseña"
    return data

  def form_valid(self, form):
    messages.success(self.request, '¡Tu contraseña ha sido actualizada exitosamente!')
    return super().form_valid(form)
