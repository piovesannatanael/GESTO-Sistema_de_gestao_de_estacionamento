from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from pagamentos.forms import PagamentoForm
from veiculos.models import Veiculo
from .models import Modalidade
from pagamentos_modal.models import PagamentoModalidade  # Ajuste se o nome do app for diferente



class ModalidadeListView(ListView):

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
        # Garante que a modalidade exista para cada veículo, para evitar erros no template.
        for veiculo in context['veiculos']:
            Modalidade.objects.get_or_create(veiculo=veiculo)
        return context


class PagarModalidadeView(View):
    """
    Processa o pagamento de uma modalidade específica.
    """
    template_name = 'modalidades/pagamento_modalidade.html'

    def get(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        # Preenche o formulário com o valor a ser pago (com multa, se aplicável)
        form = PagamentoForm(initial={'valor_pago': modalidade.valor_com_multa})

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

    def post(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoForm(request.POST)

        if form.is_valid():
            # Cria o registro do pagamento
            pagamento = form.save(commit=False)
            pagamento.modalidade = modalidade
            pagamento.save()

            return redirect('modalidades:modalidade_list')

        # Se o formulário for inválido, renderiza a página novamente com os erros
        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

