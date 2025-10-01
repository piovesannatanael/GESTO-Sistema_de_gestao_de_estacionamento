from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from .models import Estadia
from .forms import EstadiaChegadaForm, EstadiaSaidaForm

class EstadiaChegadaCreateView(CreateView):
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_chegada.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Chegada de Veículo'
        context['botao_texto'] = 'Registrar Entrada'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Entrada de veículo registrada com sucesso!")
        return super().form_valid(form)

class EstadiaSaidaUpdateView(UpdateView):
    model = Estadia
    form_class = EstadiaSaidaForm
    template_name = 'estadia_saida.html'
    success_url = reverse_lazy('estada_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Registrar Saída do Veículo: {self.object.veiculo.placa}'
        context['botao_texto'] = 'Confirmar Saída'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Saída de veículo registrada com sucesso!")
        return super().form_valid(form)

class EstadiaListView(ListView):
    model = Estadia
    template_name = 'estadias.html'
    context_object_name = 'estadas'
    paginate_by = 12

    def get_queryset(self):
        return Estadia.objects.filter(finalizada=False).select_related('veiculo', 'vaga', 'cliente')

class EstadiaDetailView(DetailView):
    model = Estadia
    template_name = 'estadias_detail.html'
    context_object_name = 'estadias'

class EstadiaDeleteView(DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

    def form_valid(self, form):
        messages.success(self.request, "Registro de estada excluído com sucesso!")
        return super().form_valid(form)

