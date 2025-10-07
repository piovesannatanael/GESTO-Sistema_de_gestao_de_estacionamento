from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from pagamentos_avulso.forms import PagamentoAvulsoForm
from veiculos.models import Veiculo
from .models import Modalidade


class ModalidadeListView(PermissionRequiredMixin, ListView):
    permission_required = 'modalidades.view_modalidade'
    permission_denied_message = 'Visualizar modalidade'
    model = Veiculo
    template_name = 'modalidades/modalidade_list.html'
    context_object_name = 'veiculos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Veiculo.objects.exclude(plano='horario_avulso')
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(placa__icontains=buscar)

        return queryset.order_by('placa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for veiculo in context['veiculos']:
            Modalidade.objects.get_or_create(veiculo=veiculo)
        return context


class PagarModalidadeView(View):

    template_name = 'modalidades/pagamento_modalidade.html'

    def get(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoAvulsoForm(initial={'valor_pago': modalidade.valor_com_multa})

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

    def post(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoAvulsoForm(request.POST)

        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.modalidade = modalidade
            pagamento.save()

            return redirect('modalidades:modalidades')

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

