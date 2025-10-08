import logging
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.utils import timezone
from estadias.models import Estadia
from .models import PagamentoAvulso
from .forms import PagamentoAvulsoForm


class ProcessarPagamentoView(View):
    template_name = 'pagamento_avulso.html'

    def _get_context(self, request, estada_avulso_pk, form=None):
        estada = get_object_or_404(Estadia, pk=estada_avulso_pk)
        pagamento, created = PagamentoAvulso.objects.get_or_create(estadia=estada, defaults={'metodo': 'PIX'})

        if created or pagamento.valor_final is None:
            valores = pagamento.calcular_valores()
            pagamento.valor_bruto = valores['valor_bruto']
            pagamento.desconto_aplicado = valores['desconto']
            pagamento.valor_final = valores['valor_final']
            pagamento.save()

        if not estada.data_saida:
            return None

        duracao = estada.data_saida - estada.data_chegada
        total_seconds = int(duracao.total_seconds())
        duracao_dias = total_seconds // 86400
        duracao_horas = (total_seconds % 86400) // 3600
        duracao_minutos = (total_seconds % 3600) // 60

        if not form:
            form = PagamentoAvulsoForm(instance=pagamento)

        context = {
            'form': form,
            'pagamento': pagamento,
            'estada': estada,
            'duracao_dias': duracao_dias,
            'duracao_horas': duracao_horas,
            'duracao_minutos': duracao_minutos,
        }
        return context

    def get(self, request, estada_avulso_pk):
        context = self._get_context(request, estada_avulso_pk)
        if context is None:
            return redirect('estadias')
        return render(request, self.template_name, context)

    def post(self, request, estada_avulso_pk):
        context = self._get_context(request, estada_avulso_pk)
        if context is None:
            return redirect('estadias')

        pagamento = context['pagamento']
        form = PagamentoAvulsoForm(request.POST, instance=pagamento)

        if form.is_valid():
            pagamento_atualizado = form.save()
            metodo = (pagamento_atualizado.metodo or '').upper()

            if metodo == 'PIX':
                return redirect('pagamentos_avulso:pagamento_pix', pagamento_pk=pagamento_atualizado.pk)
            elif metodo == 'CARTAO':
                return redirect('pagamentos_avulso:pagamento_cartao', pagamento_pk=pagamento_atualizado.pk)
            else:
                return redirect('pagamentos_avulso:pagamento_concluido', pagamento_pk=pagamento_atualizado.pk)

        return render(request, self.template_name, context)


class PagamentoPixView(View):
    template_name = 'pagamento_modal_pix.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoAvulso, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoCartaoView(View):
    template_name = 'pagamento_modal_cartao.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoAvulso, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoConcluidoView(View):
    template_name = 'pagamento_modal_concluido.html'
    logger = logging.getLogger(__name__)

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoAvulso, pk=pagamento_pk)

        if pagamento.status != 'PAGO':
            pagamento.status = 'PAGO'
            pagamento.data_pagamento = timezone.now()
            pagamento.save()

            self.enviar_email_recibo_avulso(pagamento)

        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)

    def enviar_email_recibo_avulso(self, pagamento):
        try:
            estadia = pagamento.estadia
            cliente = estadia.cliente

            if not cliente or not cliente.email:
                self.logger.warning(f"Pagamento (ID: {pagamento.pk}) sem cliente ou e-mail associado.")
                return False

            dados = {
                'cliente_nome': cliente.nome,
                'veiculo_placa': estadia.veiculo.placa,
                'veiculo_modelo': estadia.veiculo.modelo,
                'data_chegada': estadia.data_chegada,
                'data_saida': estadia.data_saida,
                'valor_bruto': pagamento.valor_bruto,
                'desconto_aplicado': pagamento.desconto_aplicado,
                'valor_final': pagamento.valor_final,
                'metodo_pagamento': pagamento.get_metodo_display(),
                'data_pagamento': pagamento.data_pagamento,
            }

            texto_email = render_to_string('emails/recibo_pgto_avulso.txt', dados)
            html_email = render_to_string('emails/recibo_pgto_avulso.html', dados)
            recipient = [cliente.email]

            send_mail(
                subject='GESTO - Recibo de Pagamento',
                message=texto_email,
                from_email='piovesannatanael@gmail.com',
                recipient_list=recipient,
                html_message=html_email,
                fail_silently=False
            )
            self.logger.info(f"E-mail de recibo enviado para {recipient} (Pagamento ID: {pagamento.pk})")
            return True
        except Exception as e:
            self.logger.exception(f"Falha ao enviar e-mail de recibo para o pagamento {pagamento.pk}: {e}")
            return False