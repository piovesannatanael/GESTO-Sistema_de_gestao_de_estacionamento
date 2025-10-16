from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from estadias.models import Estadia
from .forms import PagamentoModalForm


class ProcessarPagamentoModalView(View):
    form_template_name = 'processar_pagamento_modal.html'

    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estada_modal_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)
        veiculo = estadia.veiculo

        custo_base = 0.0
        data_validade = None

        if veiculo.plano:
            custo_base = float(veiculo.plano.valor)
            if 'mensal' in veiculo.plano.nome.lower():
                data_validade = timezone.now() + timedelta(days=30)
            elif 'semanal' in veiculo.plano.nome.lower():
                data_validade = timezone.now() + timedelta(days=7)
        else:
            messages.error(request, "Erro: Este veículo não possui um plano de modalidade para processamento.")
            return redirect('estadias')

        form = PagamentoModalForm()
        context = {
            'estadia': estadia,
            'veiculo': veiculo,
            'form': form,
            'custo_base': custo_base,
            'data_validade': data_validade,
        }
        return render(request, self.form_template_name, context)

    def post(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estada_modal_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)
        veiculo = estadia.veiculo

        form = PagamentoModalForm(request.POST)

        custo_base = float(veiculo.plano.valor) if veiculo.plano else 0.0

        if form.is_valid():
            cleaned_data = form.cleaned_data
            desconto_obj = cleaned_data.get('desconto')
            extra_obj = cleaned_data.get('extra')
            forma_pagamento = cleaned_data.get('forma_pagamento')

            valor_extra = float(extra_obj.valor) if extra_obj and extra_obj.tipo == 'FIXO' else 0.0
            subtotal = custo_base + valor_extra

            valor_desconto_selecionado = 0.0
            if desconto_obj:
                if desconto_obj.tipo == 'FIXO':
                    valor_desconto_selecionado = float(desconto_obj.valor)
                elif desconto_obj.tipo == 'PERCENTUAL':
                    valor_desconto_selecionado = subtotal * (float(desconto_obj.valor) / 100.0)

            # Desconto Funcionario

            if estadia.funcionario.cpf == estadia.cliente.cpf:
                desconto_funcionario = subtotal * 0.20
                messages.info(request, "Desconto de 20% para funcionário aplicado!")
            else:
                desconto_funcionario = 0.0

                # Desconto pix e dinheiro
            if forma_pagamento == 'PIX' or forma_pagamento == 'DINHEIRO':
                desconto_pagamento = subtotal * 0.15
                messages.info(request, "Desconto de 15% para pagamentos!")
            else:
                desconto_pagamento = 0.0


            total_descontos = valor_desconto_selecionado + desconto_pagamento + desconto_funcionario
            total_final = subtotal - total_descontos

            estadia.valor_total = max(0.0, total_final)
            estadia.forma_pagamento = forma_pagamento
            estadia.save()

            if forma_pagamento == 'PIX':
                return redirect('pagamento_final:pagamento_pix', estadia_pk=estadia.pk)
            elif forma_pagamento == 'CREDITO':
                return redirect('pagamento_final:pagamento_credito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DEBITO':
                return redirect('pagamento_final:pagamento_debito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DINHEIRO':
                return redirect('pagamento_final:pagamento_dinheiro', estadia_pk=estadia.pk)

        if veiculo.plano.nome.lower() == 'mensal':
            data_validade = timezone.now() + timedelta(days=30)
        elif veiculo.plano.nome.lower() == 'semanal':
            data_validade = timezone.now() + timedelta(days=7)
        elif veiculo.plano.nome.lower() == 'diaria':
            data_validade = timezone.now() + timedelta(days=2)
        else:
            data_validade = timezone.now()
        context = {
            'estadia': estadia,
            'veiculo': veiculo,
            'form': form,
            'custo_base': custo_base,
            'data_validade': data_validade,
        }
        return render(request, self.form_template_name, context)