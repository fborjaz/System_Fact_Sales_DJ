from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
  template_name = 'components/home.html'

  def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    context = {"title1": "IC - Inicio",
               "title2": "Corporacion el Rosado"}

    return context
