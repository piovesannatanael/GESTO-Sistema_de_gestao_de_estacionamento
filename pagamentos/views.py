# pagamentos/views.py
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import PagamentoForm
from .models import Pagamento


class PagamentosView(ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(estadia__id__icontains=buscar) |
                Q(forma__icontains=buscar) |
                Q(valor_total__icontains=buscar)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar'] = self.request.GET.get('buscar', '')
        return context


class PagamentoCreateView(SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento cadastrado com sucesso!'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


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
    success_message = 'Pagamento excluído com sucesso!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)