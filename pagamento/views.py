from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pagamento.forms import PagamentoForm
from pagamento.models import Pagamento


class PagamentosView(ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 1

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(data__icontains=buscar) |
                Q(forma__icontains=buscar)
            )
        return qs

class PagamentoCreateView(SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento cadastrado com sucesso!'

class PagamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento alterado com sucesso!'

class PagamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Pagamento
    template_name = 'pagamento_apagar.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento excluido com sucesso!'

