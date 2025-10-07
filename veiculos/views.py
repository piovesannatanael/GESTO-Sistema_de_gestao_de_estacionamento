from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from estadias.models import Estadia
from .forms import VeiculoModelForm
from .models import Veiculo


class VeiculosView(PermissionRequiredMixin, ListView):
    permission_required = 'veiculos.view_veiculo'
    permission_denied_message = 'Visualizar veiculos'
    model = Veiculo
    template_name = 'veiculos.html'
    context_object_name = 'veiculos'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('clientes')
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(
                Q(placa__icontains=buscar) |
                Q(clientes__nome__icontains=buscar) |
                Q(clientes__empresa__icontains=buscar)
            ).distinct()
        return qs


class VeiculoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'veiculos.add_veiculo'
    permission_denied_message = 'Cadastrar veiculos'
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo cadastrado com sucesso!'


class VeiculoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'veiculos.change_veiculo'
    permission_denied_message = 'Atualizar veiculos'
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo atualizado com sucesso!'


class VeiculoDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'veiculos.delete_veiculo'
    permission_denied_message = 'Excluir veiculos'
    model = Veiculo
    template_name = 'veiculo_apagar.html'
    success_url = reverse_lazy('veiculos')

    def post(self, request, *args, **kwargs):
        veiculo = self.get_object()
        if Estadia.objects.filter(veiculo=veiculo, finalizada=False).exists():
            messages.error(request,
                           f'O veículo de placa "{veiculo.placa}" não pode ser apagado pois possui uma estada ativa.')
            return redirect('veiculos')

        messages.success(request, f'O veículo de placa "{veiculo.placa}" foi apagado com sucesso.')
        return super().post(request, *args, **kwargs)

