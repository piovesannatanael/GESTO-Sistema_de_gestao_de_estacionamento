from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from veiculos.forms import VeiculoModelForm
from veiculos.models import Veiculo


class VeiculosView(ListView):
    model = Veiculo
    template_name = 'veiculos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VeiculosView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum produto cadastrado!')

class VeiculoAddView(SuccessMessageMixin, CreateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo cadastrado com sucesso!'


#     criar filtro com join para mostar cliente


class VeiculoUpdateView(SuccessMessageMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo atualizado com sucesso!'

class VeiculoDeleteView(SuccessMessageMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculo_apagar.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo excluído com sucesso!'