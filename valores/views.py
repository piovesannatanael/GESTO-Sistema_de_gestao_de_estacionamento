from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from valores.forms import PlanoForm, DescontoForm, ExtraForm
from valores.models import Plano, Desconto, Extra
from veiculos.models import Veiculo


class PlanosView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_planos"
    permission_denied_required = "Visualizar planos"
    model = Plano
    template_name = "planos/planos.html"
    context_object_name = "planos"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(plano__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

class PlanoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_plano"
    permission_denied_required = "Cadastrar plano"
    model = Plano
    form_class = PlanoForm
    template_name = "planos/planos_form.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano cadastrado com sucesso."

class PlanoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_plano"
    permission_denied_required = "Atualizar plano."
    model = Plano
    form_class = PlanoForm
    template_name = "planos/planos_form.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano atualizado com sucesso."

class PlanoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_plano"
    permission_denied_message = "Apagar plano"
    model = Plano
    template_name = "planos/plano_apagar.html"
    success_url = reverse_lazy('planos')
    success_message = "Plano apagado com sucesso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano_obj = self.get_object()
        contagem = Veiculo.objects.filter(plano=plano_obj.plano).count()
        context['veiculos_count'] = contagem
        return context


class DescontosView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_descontos"
    permission_denied_required = "Visualizar descontos"
    model = Desconto
    template_name = "descontos/descontos.html"
    context_object_name = "descontos"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(plano__icontains=buscar) |
                Q(qtd_rodas__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

class DescontoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_desconto"
    permission_denied_required = "Cadastrar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_form.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto cadastrado com sucesso."

class DescontoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.update_desconto"
    permission_denied_required = "Atualizar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_form.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto atualizado com sucesso."

class DescontoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_desconto"
    permission_denied_required = "Apagar desconto"
    model = Desconto
    form_class = DescontoForm
    template_name = "descontos/desconto_apagar.html"
    success_url = reverse_lazy('descontos')
    success_message = "Desconto apagado com sucesso."


class ExtraView(PermissionRequiredMixin, ListView):
    permission_required = "valores.view_extra"
    permission_denied_message = "Listar valores extras"
    model = Extra
    template_name = "extras/extras.html"
    context_object_name = "extras"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return qs

class ExtraCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "valores.add_extra"
    permission_denied_message = "Cadastrar valor extra"
    model = Extra
    form_class = ExtraForm
    template_name = "extras/extra_form.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra cadastrado com sucesso."

class ExtraUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "valores.change_extra"
    permission_denied_message = "Atualizar valor extra"
    model = Extra
    form_class = ExtraForm
    template_name = "extras/extra_form.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra atualizado com sucesso."

class ExtraDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "valores.delete_extra"
    permission_denied_message = "Apagar valor extra"
    model = Extra
    template_name = "extras/extra_apagar.html"
    success_url = reverse_lazy('extras')
    success_message = "Valor extra apagado com sucesso."