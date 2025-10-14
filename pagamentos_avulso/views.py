# Em: pagamentos_avulso/views.py
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

        custo_base = 0
        duracao_horas = estadia.calcular_duracao_em_horas() + 1


        if estadia.veiculo and estadia.veiculo.categoria_cnh:
            valor_por_hora = estadia.veiculo.categoria_cnh.valor_hora
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
        custo_base = 0

        try:
            duracao_horas = estadia.calcular_duracao_em_horas()
            preco_categoria = Categoria.objects.get(cnh=estadia.veiculo.categoria_cnh.cnh, status=True)
            custo_base = duracao_horas * preco_categoria.valor_hora
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

            valor_extra = 0
            if extra_obj:
                if extra_obj.tipo == 'FIXO':
                    valor_extra = extra_obj.valor
                elif extra_obj.tipo == 'PERCENTUAL':
                    valor_extra = custo_base * (extra_obj.valor / 100)

            subtotal = custo_base + valor_extra

            valor_desconto = 0
            if desconto_obj:
                if desconto_obj.tipo == 'FIXO':
                    valor_desconto = desconto_obj.valor
                elif desconto_obj.tipo == 'PERCENTUAL':
                    valor_desconto = subtotal * (desconto_obj.valor / 100)

            total_final = subtotal - valor_desconto

            estadia.valor_total = max(0, total_final)
            estadia.save()

            if forma_pagamento == 'PIX':
                return redirect('pagamento_final:pagamento_pix', estadia_pk=estadia.pk)
            elif forma_pagamento == 'CREDITO':
                return redirect('pagamento_final:pagamento_credito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DEBITO':
                return redirect('pagamento_final:pagamento_debito', estadia_pk=estadia.pk)
            elif forma_pagamento == 'DINHEIRO':
                return redirect('estadia_finalizar', pk=estadia.pk)

        context = {
            'estadia': estadia,
            'form': form,
            'custo_base': custo_base,

        }
        return render(request, self.form_template_name, context)