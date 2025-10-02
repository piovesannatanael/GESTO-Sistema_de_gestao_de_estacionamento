from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from .models import Estadia
from .forms import EstadiaChegadaForm, EstadiaSaidaForm


class EstadiaListView(ListView):
    model = Estadia
    template_name = 'estadias.html'
    context_object_name = 'object_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().filter(finalizada=False).select_related(
            'veiculo', 'cliente', 'vaga'
        )
        buscar = self.request.GET.get('buscar')

        if buscar:
            queryset = queryset.filter(
                Q(veiculo__placa__icontains=buscar) |
                Q(veiculo__modelo__icontains=buscar) |
                Q(cliente__nome__icontains=buscar) |
                Q(cliente__empresa__icontains=buscar) |
                Q(vaga__codigo__icontains=buscar)
            )

        return queryset.order_by('-data_chegada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar'] = self.request.GET.get('buscar', '')
        return context


class EstadiaChegadaCreateView(CreateView):
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registrar Chegada de Veículo"
        return context


class EstadiaChegadaUpdateView(UpdateView):
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Dados da Chegada"
        return context

class EstadiaDeleteView(DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

class EstadiaSaidaUpdateView(UpdateView):
    model = Estadia
    form_class = EstadiaSaidaForm
    template_name = 'estadia_saida.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registrar Saída de Veículo"
        return context

    def get_success_url(self):
        """
        CORREÇÃO: Após salvar a data de saída, redireciona para a tela de pagamento
        passando o ID da estada que acabamos de atualizar.
        """
        # Assumindo que a URL de pagamento se chama 'pagamento_processar' e recebe 'estada_pk'
        return reverse('pagamentos', kwargs={'estada_pk': self.object.pk})

# class EstadiaDetailView(DetailView):
#     model = Estadia
#     template_name = 'estadias/estada_detail.html'




