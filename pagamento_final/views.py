from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views import View
from estadias.models import Estadia


class PagamentoDinheiroView(View):
    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        context = {
            'estadia': estadia,
        }
        return render(request, 'pagamento_dinheiro.html', context)

class PagamentoPixView(View):
    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        context = {
            'estadia': estadia,
            'valor_final': estadia.valor_total,
        }
        return render(request, 'pagamento_pix.html', context)


class PagamentoCreditoView(View):
    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        context = {
            'estadia': estadia,
            'valor_final': estadia.valor_total,
        }
        return render(request, 'pagamento_credito.html', context)


class PagamentoDebitoView(View):
    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        context = {
            'estadia': estadia,
            'valor_final': estadia.valor_total,
        }
        return render(request, 'pagamento_debito.html', context)


class PagamentoConcluidoView(View):

    def enviar_recibo(self, estadia):
        try:
            if not estadia.cliente or not estadia.cliente.email:
                print(f"Não foi possível enviar e-mail: cliente ou e-mail não cadastrado para estadia {estadia.pk}.")
                return False
            recipient = [estadia.cliente.email]
            context = {'estadia': estadia}

            html_message = render_to_string('emails/recibo.html', context)
            plain_message = render_to_string('emails/texto_recibo.txt', context)

            send_mail(
                subject='GESTO - Recibo do seu Pagamento',
                message=plain_message,
                from_email='piovesannatanael@gmail.com',
                recipient_list=recipient,
                html_message=html_message,
                fail_silently=False
            )
            print(f"E-mail de texto_recibo enviado com sucesso para {recipient}.")
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail para estadia {estadia.pk}: {e}")
            return False

    def post(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        estadia.finalizada = True
        estadia.save()

        if estadia.vaga:
            estadia.vaga.status = 'livre'
            estadia.vaga.save()

        self.enviar_recibo(estadia)

        messages.success(request, "Pagamento confirmado e estadia finalizada!")
        context = {'estadia': estadia}

        return render(request, 'pagamento_concluido.html', context)
