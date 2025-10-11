from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import ValoresModelForm
from .models import Valores

class ValoresView(PermissionRequiredMixin, ListView):
    permission_required = 'valores.view_valores'
    permission_denied_message = 'Visualizar valores'
    model = Valores
    template_name = 'valores.html'

class ValoresAddView(PermissionRequiredMixin, SuccessMessageMixin,CreateView):
    permission_required = 'valores.add_valor'
    permission_denied_message = 'Cadastrar valores'
    model = Valores
    form_class = ValoresModelForm
    template_name = 'valores_form.html'
    success_url = reverse_lazy('valores')
    success_message = 'Valores criados com sucesso'

class ValoresUpdateView(PermissionRequiredMixin, SuccessMessageMixin,UpdateView):
    permission_required = 'valores.update_valor'
    permission_denied_message = 'Atualizar valores'
    model = Valores
    form_class = ValoresModelForm
    template_name = 'valores_form.html'
    success_url = reverse_lazy('valores')
    success_message = 'Valores atualizados com sucesso'

class ValoresDeleteView(PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
    permission_required = 'valores.delete_valor'
    permission_denied_message = 'Apagar valores'
    model = Valores
    template_name = 'valores_apagar.html'
    success_url = reverse_lazy('valores')
    success_message = 'Valores apagados com sucesso'