from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from clientes.models import ClientePJ, ClientePF
from veiculos.forms import VeiculoModelForm
from veiculos.models import Veiculo


class VeiculosView(ListView):
    model = Veiculo
    template_name = 'veiculos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VeiculosView, self).get_queryset()
        if buscar:
            qs = qs.filter(placa__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum veiculo cadastrado!')


class VeiculoAddView(SuccessMessageMixin, CreateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo cadastrado com sucesso!'

    def form_valid(self, form):
        cliente_str = form.cleaned_data['cliente_choice']
        model_str, object_id = cliente_str.split('_')

        if model_str == 'clientepf':
            model = ClientePF
        else:
            model = ClientePJ

        content_type = ContentType.objects.get_for_model(model)

        form.instance.content_type = content_type
        form.instance.object_id = int(object_id)

        return super().form_valid(form)


class VeiculoUpdateView(SuccessMessageMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo atualizado com sucesso!'

    def form_valid(self, form):
        cliente_str = form.cleaned_data.get('cliente_choice')
        tipo, pk_str = cliente_str.split('_', 1)
        pk = int(pk_str)

        if tipo == 'clientepf':
            model = ClientePF
        else:
            model = ClientePJ

        content_type = ContentType.objects.get_for_model(model)

        form.instance.content_type = content_type
        form.instance.object_id = pk

        return super().form_valid(form)

class VeiculoDeleteView(SuccessMessageMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculo_apagar.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo excluído com sucesso!'