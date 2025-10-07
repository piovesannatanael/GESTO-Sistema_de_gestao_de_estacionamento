from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Veiculo
from .forms import VeiculoModelForm

class VeiculosView(PermissionRequiredMixin, ListView):
    permission_required = 'veiculos.view_veiculos'
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

class VeiculoAddView(PermissionRequiredMixin, CreateView):
    permission_required = 'veiculos.add_veiculos'
    permission_denied_message = 'Cadastrar veiculos'
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo cadastrado com sucesso!'

class VeiculoUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'veiculos.update_veiculos'
    permission_denied_message = 'Atualizar veiculos'
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo atualizado com sucesso!'

class VeiculoDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'veiculos.delete_veiculos'
    permission_denied_message = 'Excluir veiculos'
    model = Veiculo
    template_name = 'veiculo_apagar.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo excluído com sucesso!'