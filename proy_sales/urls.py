# from django.conf import settings
# from django.conf.urls.static import static
# from app.core import views as core
# from django.contrib import admin
# from django.urls import path, include
# from app.core.views.home import HomeTemplateView
# from app.core.views.modulos import ModuloTemplateView
# from django.contrib.auth import views as auth_views

# urlpatterns = [ 
#     path('admin/', admin.site.urls),
#     path('',HomeTemplateView.as_view(), name='home'),
#     path('modulos/',ModuloTemplateView.as_view(), name='modulos'),
#     path('security/', include('app.security.urls', namespace='security')),
#     path('core/', include('app.core.urls', namespace='core')),
#     # path('signup/', core.signup, name='signup'),
#     # path('logout/', core.signout, name='logout'),
#     # path('signin/', core.signin, name='signin'),
#     # path('profile/', views.profile, name='profile'),
#     # path('profile/update/', views.update_profile, name='update_profile'),

#     # path('', include('app.core.urls', namespace='core')),
#     # path('purchase/', include('app.purchase.urls')),
#       path('reset-password/', auth_views.PasswordResetView.as_view(
#         template_name='registration/password_reset_form.html',
#         email_template_name='registration/password_reset_email.html',
#         subject_template_name='registration/password_reset_subject.txt'
#     ), name='password_reset'),

#     path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='registration/password_reset_done.html'
#     ), name='password_reset_done'),

#     path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
#         template_name='registration/password_reset_confirm.html'
#     ), name='password_reset_confirm'),

#     path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
#         template_name='registration/password_reset_complete.html'
#     ), name='password_reset_complete'),

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app.core.views.home import HomeTemplateView
from app.core.views.modulos import ModuloTemplateView
# from app.core.views import modulos

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', HomeTemplateView.as_view(), name='home'),
                path('modulos/', ModuloTemplateView.as_view(), name='modulos'),
                path('security/', include('app.security.urls', namespace='security')),
                path('core/', include('app.core.urls', namespace='core')),
                path('sales/', include('app.sales.urls', namespace='sales')),
                path('purcharse/', include('app.purcharse.urls', namespace='purchase')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
