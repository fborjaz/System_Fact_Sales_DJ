from django.urls import path
from app.security.views import auth
from django.conf import settings
from django.conf.urls.static import static
from app.core.views.home import HomeTemplateView

app_name = "security"
urlpatterns = []

urlpatterns += [
                 path('auth/login/', auth.SigninView.as_view(), name="auth_login"),
                 path('auth/logout/', auth.SignoutView.as_view(), name='auth_logout'),
                 path('auth/signup/', auth.SignupView.as_view(), name='auth_signup'),
                 path('auth/profile/', auth.ProfileView.as_view(), name='auth_profile'),
                 path('auth/change_password/', auth.ChangePasswordView.as_view(), name='auth_change_password'),
                 path('auth/update_profile/', auth.UpdateProfileView.as_view(), name='auth_update_profile'),
                 path('', HomeTemplateView.as_view(), name='home'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)