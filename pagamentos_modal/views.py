import logging
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.utils import timezone
from estadias.models import Estadia
from .models import PagamentoModal
from .forms import PagamentoModalForm


class ProcessarPagamentoModalView(View):
    template_name = 'pagamento_modal.html'

    def _get_context(self, request, estada_pk, form=None):
        estadia = get_object_or_404(Estadia, pk=estada_pk)

        pagamento, created = PagamentoModal.objects.get_or_create(
            estadia=estadia,
            defaults={
                'plano_contratado': estadia.plano,
                'metodo': 'PIX'
            }
        )

        if not form:
            form = PagamentoModalForm(instance=pagamento)

        context = {
            'form': form,
            'pagamento': pagamento,
            'estadia': estadia,
        }
        return context

    def get(self, request, estada_pk):
        context = self._get_context(request, estada_pk)
        return render(request, self.template_name, context)

    def post(self, request, estada_pk):
        context = self._get_context(request, estada_pk)
        pagamento = context['pagamento']
        form = PagamentoModalForm(request.POST, instance=pagamento)

        if form.is_valid():
            pagamento_atualizado = form.save()
            metodo = (pagamento_atualizado.metodo or '').upper()

            if metodo == 'PIX':
                return redirect('pagamento_modal_pix', pagamento_pk=pagamento_atualizado.pk)
            elif metodo == 'CARTAO':
                return redirect('pagamento_modal_cartao', pagamento_pk=pagamento_atualizado.pk)
            else:
                return redirect('pagamento_modal_concluido', pagamento_pk=pagamento_atualizado.pk)

        return render(request, self.template_name, context)


class PagamentoPixModalView(View):
    template_name = 'pagamento_pix.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoCartaoModalView(View):
    template_name = 'pagamento_cartao.html'

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)
        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


class PagamentoConcluidoModalView(View):
    template_name = 'pagamento_concluido.html'
    logger = logging.getLogger(__name__)

    def get(self, request, pagamento_pk):
        pagamento = get_object_or_404(PagamentoModal, pk=pagamento_pk)

        if pagamento.status != 'PAGO':
            pagamento.status = 'PAGO'
            pagamento.data_pagamento = timezone.now()
            pagamento.save()

            self.enviar_email_recibo_modal(pagamento)

        context = {'pagamento': pagamento}
        return render(request, self.template_name, context)


logger = logging.getLogger(__name__)

def enviar_email_recibo_modal(pagamento):
    try:
        estadia = pagamento.estadia
        cliente = estadia.cliente

        if not cliente or not cliente.email:
            logger.warning(f"Pagamento Modal (ID: {pagamento.pk}) não tem cliente ou e-mail associado para envio.")
            return False

        dados = {
            'cliente_nome': cliente.nome,
            'veiculo_placa': estadia.veiculo.placa,
            'veiculo_modelo': estadia.veiculo.modelo,
            'data_chegada': estadia.data_chegada,
            'data_saida': estadia.data_saida,
            'plano_contratado': pagamento.get_plano_contratado_display(),  # Específico do PagamentoModal
            'valor_bruto': pagamento.valor_bruto,
            'desconto_aplicado': pagamento.desconto_aplicado,
            'valor_final': pagamento.valor_final,
            'metodo_pagamento': pagamento.get_metodo_display(),
            'data_pagamento': pagamento.data_pagamento,
        }

        texto_email = render_to_string('emails/recibo_modal.txt', dados)
        html_email = render_to_string('emails/recibo_modal.html', dados)
        recipient = [cliente.email]

        send_mail(
            subject='GESTO - Recibo de Pagamento de Plano',
            message=texto_email,
            from_email='piovesannatanael@gmail.com',
            recipient_list=recipient,
            html_message=html_email,
            fail_silently=False
        )
        logger.info(f"E-mail de recibo de modalidade enviado para {recipient} (Pagamento ID: {pagamento.pk})")
        return True
    except Exception as e:
        logger.exception(f"Falha ao enviar e-mail de recibo para o pagamento modal {pagamento.pk}: {e}")
        return False
