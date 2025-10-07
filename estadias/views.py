from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Estadia
from .forms import EstadiaChegadaForm, EstadiaSaidaForm


class EstadiaListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'estadias.view_estadia'
    permission_denied_message = 'Visualizar estadia'
    model = Estadia
    template_name = 'estadias.html'
    context_object_name = 'object_list'
    paginate_by = 9

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


class EstadiaChegadaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'estadias.add_estadia'
    permission_denied_message = 'Cadastrar estadia'
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registar Chegada de Veículo"
        return context


class EstadiaChegadaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'estadias.update_estadia_chegada'
    permission_denied_message = 'Editar chegada'
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Dados da Chegada"
        return context


class EstadiaSaidaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'estadias.update_estadia_saida'
    permission_denied_message = 'Editar saida'
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


class EstadiaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'estadias.delete_estadia'
    permission_denied_message = 'Apagar estadia'
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

