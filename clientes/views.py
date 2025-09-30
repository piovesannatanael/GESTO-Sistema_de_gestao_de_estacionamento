from itertools import chain
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from clientes.forms import  ClientePFModelForm, ClientePJModelForm
from clientes.models import ClientePF, ClientePJ




### CRUD Clientes Pessoa Fisica

'''class ClientesPFView(ListView):
    model = ClientePF
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClientesPFView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum cliente cadastrado!')
'''
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

'''class ClientesPJView(ListView):
    model = ClientePJ
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClientesPJView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhuma empresa cadastrada!')
'''
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





def ClientesView(request):
    buscar = request.GET.get('buscar')

    clientespf_qs = ClientePF.objects.all()
    clientespj_qs = ClientePJ.objects.all()

    if buscar:
        clientespf_qs = clientespf_qs.filter(nome__icontains=buscar)
        clientespj_qs = clientespj_qs.filter(nome__icontains=buscar)

    lista_clientes = sorted(
        chain(clientespf_qs, clientespj_qs),
        key=lambda instance: instance.nome.upper()
    )

    paginator = Paginator(lista_clientes, 1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'object_list': page_obj,
        'buscar': buscar if buscar else '',
    }
    return render(request, 'clientes.html', context)





'''def ClientesView(request):
    clientespf_qs = ClientePF.objects.all().order_by('nome')
    clientespj_qs = ClientePJ.objects.all().order_by('nome')

    # Paginação (opcional) — 10 por página para cada lista
    page_pf = request.GET.get('page_pf', 1)
    page_pj = request.GET.get('page_pj', 1)

    paginator_pf = Paginator(clientespf_qs, 10)
    paginator_pj = Paginator(clientespj_qs, 10)

    clientespf = paginator_pf.get_page(page_pf)
    clientespj = paginator_pj.get_page(page_pj)

    context = {
        'clientespf': clientespf,
        'clientespj': clientespj,
        'buscar': request.GET.get('buscar', ''),
        'request': request,  # necessário para bootstrap_pagination url=request.get_full_path
    }
    return render(request, 'clientes.html', context)
'''
'''class ClientesView(TemplateView):
    template_name = 'clientes.html'
    paginate_by = 10
    context_object_name = 'clientes'  # Use 'clientes' para ser mais claro no template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pega o termo de busca da URL
        buscar = self.request.GET.get('buscar')

        # Busca e filtra a lista de Clientes PF
        clientes_pf = ClientePF.objects.all()
        if buscar:
            clientes_pf = clientes_pf.filter(nome__icontains=buscar)

        # Busca e filtra a lista de Clientes PJ
        clientes_pj = ClientePJ.objects.all()
        if buscar:
            # Lembre-se que em ClientePJ, o nome da empresa está no campo 'nome'
            clientes_pj = clientes_pj.filter(nome__icontains=buscar)

        # Adiciona as duas listas e o termo de busca ao contexto
        context['clientes_pf'] = clientes_pf
        context['clientes_pj'] = clientes_pj
        context['buscar'] = buscar if buscar else ''

        return context'''