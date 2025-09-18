from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from clientes.forms import ClienteModelForm
from clientes.models import  Cliente


class ClientesView(ListView):
    model = Cliente
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClientesView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 5)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum cliente cadastrado!')

class ClienteAddView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'

class ClienteDeleteView(SuccessMessageMixin, DeleteView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes/')
    success_message = 'Cliente excluido com sucesso!'





'''
### CRUD Clientes Pessoa Fisica

class ClientesPFView(ListView):
    model = ClientePF
    template_name = 'clientespf.html'

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

class ClientePFAddView(SuccessMessageMixin, CreateView):
    model = ClientePF
    form_class = ClientePFModelForm
    template_name = 'clientespf_form.html'
    success_url = reverse_lazy('clientespf')
    success_message = 'Cliente cadastrado com sucesso!'

class ClientePFUpdateView(SuccessMessageMixin, UpdateView):
    model = ClientePF
    form_class = ClientePFModelForm
    template_name = 'clientespf_form.html'
    success_url = reverse_lazy('clientespf')
    success_message = 'Cliente atualizado com sucesso!'

class ClientePFDeleteView(SuccessMessageMixin, DeleteView):
    model = ClientePF
    form_class = ClientePFModelForm
    template_name = 'clientespf_apagar.html'
    success_url = reverse_lazy('clientespf')
    success_message = 'Cliente excluido com sucesso!'


### CRUD Clientes Pessoa Juridica

class ClientesPJView(ListView):
    model = ClientePJ
    template_name = 'clientespj.html'

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

class ClientePJAddView(SuccessMessageMixin, CreateView):
    model = ClientePJ
    form_class = ClientePJModelForm
    template_name = 'clientespj_form.html'
    success_url = reverse_lazy('clientespj')
    success_message = 'Empresa cliente cadastrada com sucesso!'

class ClientePJUpdateView(SuccessMessageMixin, UpdateView):
    model = ClientePJ
    form_class = ClientePJModelForm
    template_name = 'clientespj_form.html'
    success_url = reverse_lazy('clientespj')
    success_message = 'Empresa cliente atualizada com sucesso!'

class ClientePJDeleteView(SuccessMessageMixin, DeleteView):
    model = ClientePJ
    form_class = ClientePJModelForm
    template_name = 'clientespj_apagar.html'
    success_url = reverse_lazy('clientespj')
    success_message = 'Empresa cliente excluída com sucesso!'

'''