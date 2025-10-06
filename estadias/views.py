from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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

    def form_valid(self, form):
        veiculo = form.cleaned_data.get('veiculo')
        if veiculo:
            form.instance.plano = veiculo.plano
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registar Chegada de Veículo"
        return context


class EstadiaChegadaUpdateView(UpdateView):
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')

    def form_valid(self, form):
        veiculo = form.cleaned_data.get('veiculo')
        if veiculo:
            form.instance.plano = veiculo.plano
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Dados da Chegada"
        return context


class EstadiaSaidaUpdateView(UpdateView):
    model = Estadia
    form_class = EstadiaSaidaForm
    template_name = 'estadia_saida.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registar Saída de Veículo"
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pagamento_processar', kwargs={'estada_pk': self.object.pk})


class EstadiaDeleteView(DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

