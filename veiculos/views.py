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
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum produto cadastrado!')


class VeiculoAddView(SuccessMessageMixin, CreateView):
    model = Veiculo
    form_class = VeiculoModelForm  # Use o formulário customizado
    template_name = 'veiculo_form.html' # Troque pelo nome do seu template
    success_url = reverse_lazy('veiculos') # Troque pela URL de sucesso
    success_message = 'Veículo cadastrado com sucesso!'

    def form_valid(self, form):
        # Pega o valor escolhido no dropdown, ex: "clientepf_5"
        cliente_str = form.cleaned_data['cliente_choice']
        model_str, object_id = cliente_str.split('_')

        # Converte a string do modelo para o modelo real
        if model_str == 'clientepf':
            model = ClientePF
        else:
            model = ClientePJ

        # Pega o ContentType correspondente ao modelo
        content_type = ContentType.objects.get_for_model(model)

        # Atribui o content_type e o object_id à instância do Veiculo
        # antes de salvá-la
        self.object = form.save(commit=False)
        self.object.content_type = content_type
        self.object.object_id = object_id
        self.object.save()

        return super().form_valid(form)

# class VeiculoAddView(SuccessMessageMixin, CreateView):
#     model = Veiculo
#     form_class = VeiculoModelForm
#     template_name = 'veiculo_form.html'
#     success_url = reverse_lazy('veiculos')
#     success_message = 'Veículo cadastrado com sucesso!'
#
#
# #     criar filtro com join para mostar cliente


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