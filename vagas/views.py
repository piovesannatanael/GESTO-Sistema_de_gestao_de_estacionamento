from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from estadias.models import Estadia
from vagas.forms import VagaModelForm
from vagas.models import Vaga


class VagasView(PermissionRequiredMixin, ListView):
    permission_required = 'vagas.view_vaga'
    permission_denied_message = 'Visualizar vaga'
    model = Vaga
    template_name = 'vagas.html'
    context_object_name = 'vagas'
    paginate_by = 5

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        estada_ativa_qs = Estadia.objects.filter(finalizada=False)

        queryset = Vaga.objects.prefetch_related(
            Prefetch('estadia_set', queryset=estada_ativa_qs, to_attr='estada_ativa')
        )

        if buscar:
            queryset = queryset.filter(
                Q(codigo__icontains=buscar) |
                Q(status__icontains=buscar)
            )
        return queryset.order_by('codigo')


class VagaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'vagas.add_vaga'
    permission_denied_message = 'Cadastrar vaga'
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga cadastrada com sucesso!'


class VagaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'vagas.update_vaga'
    permission_denied_message = 'Editar vaga'
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga alterada com sucesso!'


class VagaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'vagas.delete_vaga'
    permission_denied_message = 'Excluir vaga'
    model = Vaga
    template_name = 'vaga_apagar.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga excluída com sucesso!'

    def post(self, request, *args, **kwargs):
        vaga = self.get_object()
        if vaga.status == 'ocupada':
            messages.error(request, f'A vaga "{vaga.codigo}" está em uso e não pode ser apagada.')
            return redirect('vagas')
        return super().post(request, *args, **kwargs)
