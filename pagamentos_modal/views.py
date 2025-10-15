from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from veiculos.models import Veiculo
from .forms import PagamentoModalForm



class ProcessarPagamentoModalView(View):
    form_template_name = 'pagamentos_modal/processar_pagamento_modal.html'

    def get(self, request, *args, **kwargs):
        veiculo_pk = self.kwargs.get('veiculo_pk')
        veiculo = get_object_or_404(Veiculo, pk=veiculo_pk)

        custo_base = 0.0
        data_validade = None

        if veiculo.plano:
            custo_base = float(veiculo.plano.valor)
            if 'mensal' in veiculo.plano.nome.lower():
                data_validade = timezone.now() + timedelta(days=30)
            elif 'semanal' in veiculo.plano.nome.lower():
                data_validade = timezone.now() + timedelta(days=7)
        else:
            messages.error(request, "Este veículo não possui um plano de modalidade associado.")

        form = PagamentoModalForm()
        context = {
            'veiculo': veiculo,
            'form': form,
            'custo_base': custo_base,
            'data_validade': data_validade,
        }
        return render(request, self.form_template_name, context)

    def post(self, request, *args, **kwargs):

        pass