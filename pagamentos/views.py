from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from estadias.models import Estadia
from .models import Pagamento
from .forms import PagamentoForm


class ProcessarPagamentoView(View):
    template_name = 'pagamentos.html'

    def _get_context(self, request, estada_pk, form=None):
        estada = get_object_or_404(Estadia, pk=estada_pk)

        pagamento, created = Pagamento.objects.get_or_create(estada=estada)
        if created or not pagamento.valor_calculado:
            pagamento.valor_calculado = pagamento.calcular_valor()
            pagamento.save()

        if not estada.data_saida:
            return None

        duracao = estada.data_saida - estada.data_chegada
        total_seconds = int(duracao.total_seconds())

        duracao_dias = total_seconds // 86400
        duracao_horas = (total_seconds % 86400) // 3600
        duracao_minutos = (total_seconds % 3600) // 60

        if not form:
            form = PagamentoForm(instance=pagamento)

        context = {
            'form': form,
            'pagamento': pagamento,
            'estada': estada,
            'duracao_dias': duracao_dias,
            'duracao_horas': duracao_horas,
            'duracao_minutos': duracao_minutos,
        }
        return context

    def get(self, request, estada_pk):
        context = self._get_context(request, estada_pk)
        if context is None:
            return redirect('estadias')
        return render(request, self.template_name, context)

    def post(self, request, estada_pk):
        # Usamos uma função auxiliar para não repetir a lógica de buscar e calcular
        context = self._get_context(request, estada_pk)
        pagamento = context['pagamento']
        form = PagamentoForm(request.POST, instance=pagamento)

        if form.is_valid():
            pagamento = form.save(commit=False)
            desconto = form.cleaned_data.get('desconto') or 0
            adicional = form.cleaned_data.get('valor_adicional') or 0

            valor_base = pagamento.valor_calculado
            pagamento.valor_calculado = valor_base - desconto + adicional

            pagamento.save()

            metodo = form.cleaned_data.get('metodo')
            if metodo == 'pix':
                return redirect('pagamento_pix', pagamento_pk=pagamento.pk)
            elif metodo in ['cartao_credito', 'cartao_debito']:
                return redirect('pagamento_cartao', pagamento_pk=pagamento.pk)
            else:
                pagamento.status = 'pago'
                pagamento.save()
                return redirect('pagamento_concluido', pagamento_pk=pagamento.pk)

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

