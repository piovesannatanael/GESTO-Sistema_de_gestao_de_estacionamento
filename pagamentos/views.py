from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.utils import timezone
from estadias.models import Estadia
from .models import Pagamento
from .forms import ProcessarPagamentoForm
from decimal import Decimal


class ProcessarPagamentoView(View):
    template_name = 'pagamentos/pagamento_detail.html'

    def get(self, request, estada_pk):
        estada = get_object_or_404(Estadia, pk=estada_pk, finalizada=False)
        pagamento, created = Pagamento.objects.get_or_create(estada=estada)

        if not estada.data_saida:
            estada.data_saida = timezone.now()

        valor_calculado = pagamento.calcular_valor()
        pagamento.valor_calculado = valor_calculado
        duracao = estada.data_saida - estada.data_chegada

        form = ProcessarPagamentoForm(initial={'valor_calculado': valor_calculado})

        context = {
            'form': form,
            'pagamento': pagamento,
            'estada': estada,
            'duracao': duracao,
        }
        return render(request, self.template_name, context)

    def post(self, request, estada_pk):
        estada = get_object_or_404(Estadia, pk=estada_pk)
        pagamento = get_object_or_404(Pagamento, estada=estada)
        form = ProcessarPagamentoForm(request.POST, initial={'valor_calculado': pagamento.calcular_valor()})

        if form.is_valid():
            metodo = form.cleaned_data['metodo']
            desconto = form.cleaned_data.get('desconto') or Decimal('0.00')
            valor_adicional = form.cleaned_data.get('valor_adicional') or Decimal('0.00')

            valor_final = pagamento.calcular_valor() - desconto + valor_adicional

            pagamento.valor_calculado = valor_final
            pagamento.metodo = metodo
            # Não salva o status ainda, isso será feito na tela de pagamento final
            pagamento.save(update_fields=['valor_calculado', 'metodo'])

            if metodo == 'pix':
                return redirect('pagamento_pix', pagamento_pk=pagamento.pk)
            elif metodo in ['cartao_credito', 'cartao_debito']:
                return redirect('pagamento_cartao', pagamento_pk=pagamento.pk)
            else:  # Dinheiro
                pagamento.status = 'pago'
                pagamento.save()
                return redirect('pagamento_concluido', pagamento_pk=pagamento.pk)

        duracao = estada.data_saida - estada.data_chegada if estada.data_saida else None
        context = {
            'form': form,
            'pagamento': pagamento,
            'estada': estada,
            'duracao': duracao,
        }
        return render(request, self.template_name, context)


# --- NOVAS VIEWS PARA AS PRÓXIMAS ETAPAS ---

class PagamentoPixView(DetailView):
    model = Pagamento
    template_name = 'pagamentos/pagamento_pix.html'
    context_object_name = 'pagamento'


class PagamentoCartaoView(DetailView):
    model = Pagamento
    template_name = 'pagamentos/pagamento_cartao.html'
    context_object_name = 'pagamento'


class PagamentoConcluidoView(DetailView):
    model = Pagamento
    template_name = 'pagamentos/pagamento_concluido.html'
    context_object_name = 'pagamento'

