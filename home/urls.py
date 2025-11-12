from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy
from .views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='login.html', extra_context={'titulo':'Autenticação'}), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar_senha/', PasswordChangeView.as_view(template_name='login.html', extra_context={'titulo':'Alterar senha'},
                                                      success_url=reverse_lazy('index')), name='alterar_senha'),

]