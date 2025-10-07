from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from estadias.models import Estadia
from .models import PagamentoModal
from .forms import PagamentoModalForm  # Garanta que este form exista


class ProcessarPagamentoModalView(View):
    """
    View para processar o pagamento de estadias baseadas em planos
    (diaria, semanal, mensal).
    """
    template_name = 'pagamento_modal.html'

    def get_context_data(self, estada_pk, form=None):
        """Prepara o contexto comum para GET e POST."""
        estadia = get_object_or_404(Estadia, pk=estada_pk)

        # Se o formulário não for passado, cria um novo
        if not form:
            # Cria a instância do formulário, passando o plano da estadia como `initial`
            form = PagamentoModalForm(initial={'plano_contratado': estadia.plano})

        # Cria um objeto de pagamento temporário (sem salvar) para os cálculos
        # Isso permite que o método `calcular_valores` funcione corretamente
        pagamento_temp = PagamentoModal(
            estadia=estadia,
            plano_contratado=form.data.get('plano_contratado', estadia.plano),
            metodo=form.data.get('metodo', 'PIX')  # Usa PIX como padrão
        )
        valores_calculados = pagamento_temp.calcular_valores()

        context = {
            'form': form,
            'estadia': estadia,
            'valores': valores_calculados,
        }
        return context

    def get(self, request, estada_pk):
        context = self.get_context_data(estada_pk)
        return render(request, self.template_name, context)

    def post(self, request, estada_pk):
        form = PagamentoModalForm(request.POST)

        if form.is_valid():
            # Cria a instância do pagamento com os dados validados do formulário
            pagamento = form.save(commit=False)

            estadia = get_object_or_404(Estadia, pk=estada_pk)
            pagamento.estadia = estadia

            # O método save() do modelo já cuida de chamar calcular_valores()
            # e preencher valor_bruto, desconto_aplicado e valor_final.
            pagamento.save()

            # Aqui você pode adicionar um redirecionamento para uma página de sucesso
            # ou para processar pagamentos específicos como PIX/Cartão se desejar.
            # Por simplicidade, vamos redirecionar para uma página de conclusão.
            return redirect('pagamento_modal_concluido', pagamento_pk=pagamento.pk)

        # Se o formulário for inválido, renderiza a página novamente com os erros
        context = self.get_context_data(estada_pk, form=form)
        return render(request, self.template_name, context)


class PagamentoModalConcluidoView(View):
    """
    Página simples para mostrar a confirmação do pagamento.
    """
    template_name = 'pagamento_concluido.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)

        # Garante que a data do pagamento seja registrada
        if not pagamento.data_pagamento:
            pagamento.data_pagamento = timezone.now()
            pagamento.save(update_fields=['data_pagamento'])

        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)

class PagamentoPixView(View):
    template_name = 'pagamento_pix.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoCartaoView(View):
    template_name = 'pagamento_cartao.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoConcluidoView(View):
    template_name = 'pagamento_concluido.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)

        if pagamento.status != 'PAGO':
            pagamento.status = 'PAGO'
            pagamento.data_pagamento = timezone.now()
            pagamento.save()

        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)
