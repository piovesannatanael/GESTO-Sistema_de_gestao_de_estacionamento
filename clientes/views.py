from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import ClienteGeral
from .forms import ClienteGeralModelForm

class ClienteListView(ListView):
    model = ClienteGeral
    template_name = 'cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            # Busca por nome (PF), empresa (PJ) ou documento (CPF/CNPJ)
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(empresa__icontains=buscar) |
                Q(cpf__icontains=buscar) |
                Q(cnpj__icontains=buscar)
            )
        return qs

class ClienteCreateView(CreateView):
    model = ClienteGeral
    form_class = ClienteGeralModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('cliente_list') # URL para redirecionar após sucesso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Cadastrar Novo Cliente"
        return context

class ClienteUpdateView(UpdateView):
    model = ClienteGeral
    form_class = ClienteGeralModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Cliente"
        return context

class ClienteDeleteView(DeleteView):
    model = ClienteGeral
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')


# from itertools import chain
#
# from django.db.models import Q
# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.paginator import Paginator
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
#
# from clientes.forms import ClientePFModelForm, ClientePJModelForm
# from clientes.models import ClientePF, ClientePJ, Cliente
#
#
# class ClientesView(ListView):
#     model = Cliente
#     template_name = 'clientes.html'
#     paginate_by = 1
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         buscar = (self.request.GET.get('buscar') or '').strip()
#
#         if buscar:
#             qs = qs.filter(
#                 Q(nome__icontains=buscar) |
#                 Q(empresa__icontains=buscar) |
#                 Q(email__icontains=buscar)
#             )
#
#         if not qs.exists():
#             messages.info(self.request, 'Nenhum cliente cadastrado!')
#
#         return qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['buscar'] = self.request.GET.get('buscar', '')
#         return context
#
#
# ### CRUD Clientes Pessoa Fisica
#
# # class ClientesPFView(ListView):
# #     model = ClientePF
# #     template_name = 'clientes.html'
# #
# #     def get_queryset(self):
# #         buscar = self.request.GET.get('buscar')
# #         qs = super(ClientesPFView, self).get_queryset()
# #         if buscar:
# #             qs = qs.filter(nome__icontains=buscar)
# #
# #         if qs.count() > 0:
# #             paginator = Paginator(qs, 1)
# #             listagem = paginator.get_page(self.request.GET.get('page'))
# #             return listagem
# #         else:
# #             return messages.info(self.request, 'Nenhum cliente cadastrado!')
# #
# class ClientePFAddView(SuccessMessageMixin, CreateView):
#     model = ClientePF
#     form_class = ClientePFModelForm
#     template_name = 'clientepf_form.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Cliente cadastrado com sucesso!'
#
# class ClientePFUpdateView(SuccessMessageMixin, UpdateView):
#     model = ClientePF
#     form_class = ClientePFModelForm
#     template_name = 'clientepf_form.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Cliente atualizado com sucesso!'
#
# class ClientePFDeleteView(SuccessMessageMixin, DeleteView):
#     model = ClientePF
#     template_name = 'clientepf_apagar.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Cliente excluido com sucesso!'
# #
# #
# # ### CRUD Clientes Pessoa Juridica
# #
# class ClientePJAddView(SuccessMessageMixin, CreateView):
#     model = ClientePJ
#     form_class = ClientePJModelForm
#     template_name = 'clientepj_form.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Empresa cliente cadastrada com sucesso!'
#
# class ClientePJUpdateView(SuccessMessageMixin, UpdateView):
#     model = ClientePJ
#     form_class = ClientePJModelForm
#     template_name = 'clientepj_form.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Empresa cliente atualizada com sucesso!'
#
# class ClientePJDeleteView(SuccessMessageMixin, DeleteView):
#     model = ClientePJ
#     template_name = 'clientepj_apagar.html'
#     success_url = reverse_lazy('clientes')
#     success_message = 'Empresa cliente excluída com sucesso!'
# #
# #
# # class ClientesView(ListView):
# #     model = ClienteGeral
# #     template_name = 'clientes.html'
#
# #
# # def ClientesView(request):
# #     buscar = request.GET.get('buscar')
# #
# #     clientespf_qs = ClientePF.objects.all()
# #     clientespj_qs = ClientePJ.objects.all()
# #
# #     if buscar:
# #         clientespf_qs = clientespf_qs.filter(nome__icontains=buscar)
# #         clientespj_qs = clientespj_qs.filter(nome__icontains=buscar)
# #
# #     lista_clientes = sorted(
# #         chain(clientespf_qs, clientespj_qs),
# #         key=lambda instance: instance.nome.upper()
# #     )
# #
# #     paginator = Paginator(lista_clientes, 1)
# #     page_num = request.GET.get('page')
# #     page_obj = paginator.get_page(page_num)
# #
# #     context = {
# #         'object_list': page_obj,
# #         'buscar': buscar if buscar else '',
# #     }
# #     return render(request, 'clientes.html', context)
#
