from itertools import chain

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from clientes.forms import  ClientePFModelForm, ClientePJModelForm
from clientes.models import ClientePF, ClientePJ




### CRUD Clientes Pessoa Fisica

# class ClientesPFView(ListView):
#     model = ClientePF
#     template_name = 'clientes.html'
#
#     def get_queryset(self):
#         buscar = self.request.GET.get('buscar')
#         qs = super(ClientesPFView, self).get_queryset()
#         if buscar:
#             qs = qs.filter(nome__icontains=buscar)
#
#         if qs.count() > 0:
#             paginator = Paginator(qs, 1)
#             listagem = paginator.get_page(self.request.GET.get('page'))
#             return listagem
#         else:
#             return messages.info(self.request, 'Nenhum cliente cadastrado!')

class ClientePFAddView(SuccessMessageMixin, CreateView):
    model = ClientePF
    form_class = ClientePFModelForm
    template_name = 'clientepf_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'

class ClientePFUpdateView(SuccessMessageMixin, UpdateView):
    model = ClientePF
    form_class = ClientePFModelForm
    template_name = 'clientepf_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'

class ClientePFDeleteView(SuccessMessageMixin, DeleteView):
    model = ClientePF
    template_name = 'clientepf_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente excluido com sucesso!'


### CRUD Clientes Pessoa Juridica
class ClientesView(ListView):
    model = ClientePF or ClientePJ
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClientesView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum CLIENTE OU EMPRESA cadastrada!')


# class ClientesPJView(ListView):
#     model = ClientePJ
#     template_name = 'clientes.html'
#
#     def get_queryset(self):
#         buscar = self.request.GET.get('buscar')
#         qs = super(ClientesPJView, self).get_queryset()
#         if buscar:
#             qs = qs.filter(nome__icontains=buscar)
#
#         if qs.count() > 0:
#             paginator = Paginator(qs, 1)
#             listagem = paginator.get_page(self.request.GET.get('page'))
#             return listagem
#         else:
#             return messages.info(self.request, 'Nenhuma empresa cadastrada!')

class ClientePJAddView(SuccessMessageMixin, CreateView):
    model = ClientePJ
    form_class = ClientePJModelForm
    template_name = 'clientepj_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Empresa cliente cadastrada com sucesso!'

class ClientePJUpdateView(SuccessMessageMixin, UpdateView):
    model = ClientePJ
    form_class = ClientePJModelForm
    template_name = 'clientepj_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Empresa cliente atualizada com sucesso!'

class ClientePJDeleteView(SuccessMessageMixin, DeleteView):
    model = ClientePJ
    template_name = 'clientepj_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Empresa cliente excluída com sucesso!'


from django.shortcuts import render
from django.core.paginator import Paginator


