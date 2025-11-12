from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from estadias.models import Estadia
from .models import ClienteGeral
from .forms import ClienteGeralModelForm


class ClienteListView(PermissionRequiredMixin, ListView):
    permission_required = 'clientes.view_clientegeral'
    model = ClienteGeral
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(empresa__icontains=buscar) |
                Q(cpf__icontains=buscar) |
                Q(cnpj__icontains=buscar)
            )
        return qs


class ClienteCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'clientes.add_clientegeral'
    model = ClienteGeral
    form_class = ClienteGeralModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Cadastrar Novo Cliente"
        return context


class ClienteUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'clientes.change_clientegeral'
    model = ClienteGeral
    form_class = ClienteGeralModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Cliente"
        return context


class ClienteDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'clientes.delete_clientegeral'
    model = ClienteGeral
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')

    def post(self, request, *args, **kwargs):
        cliente = self.get_object()

        if Estadia.objects.filter(cliente=cliente, finalizada=False).exists():
            if cliente.empresa:
                nome_display = f'{cliente.nome} / {cliente.empresa}'
            else:
                nome_display = cliente.nome
            messages.error(request,
                           f'O cliente "{nome_display}" não pode ser apagado pois possui uma estada ativa.')
            return redirect('clientes')

        return super().post(request, *args, **kwargs)
