from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from veiculos.models import Veiculo
from .models import Modalidade
from pagamentos.models import PagamentoModalidade
from .forms import PagamentoModalidadeForm


class ModalidadeListView(ListView):
    """
    Lista todos os veículos que possuem planos e o status de suas modalidades,
    com funcionalidade de busca e filtro.
    """
    model = Veiculo
    template_name = 'modalidades/modalidade_list.html'
    context_object_name = 'veiculos'
    paginate_by = 9

    def get_queryset(self):
        # Começa com os veículos que têm planos
        queryset = Veiculo.objects.exclude(plano='horario_avulso')

        # Pega os parâmetros da URL
        buscar = self.request.GET.get('buscar')
        plano_filtro = self.request.GET.get('plano')

        # Aplica o filtro de busca por placa
        if buscar:
            queryset = queryset.filter(placa__icontains=buscar)

        # Aplica o filtro de plano
        if plano_filtro:
            queryset = queryset.filter(plano=plano_filtro)

        return queryset.order_by('placa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Garante que a modalidade exista para cada veículo listado
        for veiculo in context['veiculos']:
            Modalidade.objects.get_or_create(veiculo=veiculo)

        # Envia os valores dos filtros de volta para o template
        context['buscar'] = self.request.GET.get('buscar', '')
        context['plano_selecionado'] = self.request.GET.get('plano', '')
        return context


class PagarModalidadeView(View):
    """
    Processa o pagamento de uma modalidade específica.
    """
    template_name = 'modalidades/pagamento_modalidade.html'

    def get(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoModalidadeForm(initial={'valor_pago': modalidade.valor_com_multa})

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

    def post(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoModalidadeForm(request.POST)

        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.modalidade = modalidade
            pagamento.save()

            return redirect('modalidade_list')

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

