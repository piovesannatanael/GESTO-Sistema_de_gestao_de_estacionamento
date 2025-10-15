from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from estadias.models import Estadia
from valores.models import Categoria
from .forms import PagamentoAvulsoForm


class ProcessarPagamentoAvulsoView(View):
    form_template_name = 'processar_pagamento_avulso.html'

    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estada_avulso_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        custo_base = 0.0

        duracao_horas = estadia.calcular_duracao_em_horas()


        if estadia.veiculo and estadia.veiculo.categoria_cnh:

            valor_por_hora = float(estadia.veiculo.categoria_cnh.valor_hora)
            custo_base = duracao_horas * valor_por_hora
        else:
            messages.error(request, "O veículo ou sua categoria não estão definidos corretamente para esta estadia.")

        form = PagamentoAvulsoForm()

        context = {
            'estadia': estadia,
            'form': form,
            'duracao_horas': duracao_horas,
            'custo_base': custo_base,
        }
        return render(request, self.form_template_name, context)


    def post(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estada_avulso_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        form = PagamentoAvulsoForm(request.POST)
        custo_base = 0.0

        try:
            duracao_horas = estadia.calcular_duracao_em_horas()
            duracao_horas = max(1, duracao_horas)

            preco_categoria = Categoria.objects.get(cnh=estadia.veiculo.categoria_cnh.cnh, status=True)
            custo_base = duracao_horas * float(preco_categoria.valor_hora)

        except Categoria.DoesNotExist:
            messages.error(request,
                           f"Não há um preço ativo cadastrado para a categoria '{estadia.veiculo.categoria_cnh.get_cnh_display()}'")

            context = {'estadia': estadia, 'form': form, 'custo_base': custo_base}
            return render(request, self.form_template_name, context)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            desconto_obj = cleaned_data.get('desconto')
            extra_obj = cleaned_data.get('extra')
            forma_pagamento = cleaned_data.get('forma_pagamento')



            valor_extra = 0.0
            if extra_obj:
                if extra_obj.tipo == 'FIXO':
                    valor_extra = float(extra_obj.valor)
                elif extra_obj.tipo == 'PERCENTUAL':
                    valor_extra = custo_base * (float(extra_obj.valor) / 100.0)

            subtotal = custo_base + valor_extra


            valor_desconto = 0.0
            if desconto_obj:
                if desconto_obj.tipo == 'FIXO':
                    valor_desconto = float(desconto_obj.valor)
                elif desconto_obj.tipo == 'PERCENTUAL':
                    valor_desconto = subtotal * (float(desconto_obj.valor) / 100.0)

                # Desconto Funcionario

            if estadia.funcionario.cpf == estadia.cliente.cpf:
                desconto_funcionario = subtotal * 0.20
                messages.info(request, "Desconto de 20% para funcionário aplicado!")
            else:
                desconto_funcionario = 0.0

                # Desconto pix e dinheiro
            if forma_pagamento == 'PIX' or forma_pagamento == 'DINHEIRO':
                desconto_pagamento = subtotal * 0.15
                messages.info(request, "Desconto de 15% para pagamento!")
            else:
                desconto_pagamento = 0.0

                # Multa 50% estadia > 12h
            if duracao_horas > 12:
                multa_12h = subtotal * 0.5
            else:
                multa_12h = subtotal * 0.0



            total_desconto = valor_desconto + desconto_funcionario + desconto_pagamento

            total_final = subtotal - total_desconto + multa_12h


            estadia.valor_total = max(0.0, total_final)

            estadia.save()


            if forma_pagamento == 'PIX':
                return redirect('pagamento_final:pagamento_pix', estadia_pk=estadia.pk)
            elif forma_pagamento == 'CREDITO':
                return redirect('pagamento_final:pagamento_credito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DEBITO':
                return redirect('pagamento_final:pagamento_debito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DINHEIRO':
                return redirect('pagamento_final:pagamento_dinheiro', estadia_pk=estadia.pk)






        context = {
            'estadia': estadia,
            'form': form,
            'custo_base': custo_base,
            'forma_pagamento': forma_pagamento,

        }
        return render(request, self.form_template_name, context)