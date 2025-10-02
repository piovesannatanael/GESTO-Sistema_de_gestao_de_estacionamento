from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from estadias.models import Estadia
from .models import Pagamento
from .forms import PagamentoForm
from datetime import timedelta


class ProcessarPagamentoView(View):
    # CORREÇÃO: O caminho do template foi padronizado
    template_name = 'pagamentos.html'

    def get(self, request, estada_pk):
        estada = get_object_or_404(Estadia, pk=estada_pk)
        pagamento, created = Pagamento.objects.get_or_create(estada=estada)

        if not estada.data_saida:
            return redirect('estada_list')

        duracao = estada.data_saida - estada.data_chegada

        # O formulário é preenchido com os dados do pagamento
        form = PagamentoForm(instance=pagamento)

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
        form = PagamentoForm(request.POST, instance=pagamento)

        if form.is_valid():
            pagamento = form.save(commit=False)

            desconto = form.cleaned_data.get('desconto', 0)
            adicional = form.cleaned_data.get('valor_adicional', 0)
            valor_base = pagamento.calcular_valor()
            pagamento.valor_calculado = valor_base - desconto + adicional

            pagamento.save()

            metodo = form.cleaned_data.get('metodo')
            if metodo == 'pix':
                return redirect('pagamento_pix', pagamento_pk=pagamento.pk)
            elif metodo in ['cartao_credito', 'cartao_debito']:
                return redirect('pagamento_cartao', pagamento_pk=pagamento.pk)
            else:  # Dinheiro ou outros
                pagamento.status = 'pago'
                pagamento.save()
                return redirect('pagamento_concluido', pagamento_pk=pagamento.pk)

        duracao = estada.data_saida - estada.data_chegada
        context = {
            'form': form,
            'pagamento': pagamento,
            'estada': estada,
            'duracao': duracao,
        }
        return render(request, self.template_name, context)


class PagamentoPixView(View):
    template_name = 'pagamento_pix.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(Pagamento, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoCartaoView(View):
    template_name = 'pagamento_cartao.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(Pagamento, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoConcluidoView(View):
    template_name = 'pagamento_concluido.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(Pagamento, pk=pagamento_pk)

        if pagamento.status != 'pago':
            pagamento.status = 'pago'
            pagamento.save()

        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)



