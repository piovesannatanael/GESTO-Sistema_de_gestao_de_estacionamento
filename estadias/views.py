from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.generic.base import logger

from .models import Estadia
from .forms import EstadiaChegadaForm, EstadiaSaidaForm


class EstadiaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'estadias.view_estadia'
    model = Estadia
    template_name = 'estadias.html'
    context_object_name = 'object_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'veiculo', 'cliente', 'vaga'
        )
        buscar = self.request.GET.get('buscar')

        if buscar:
            queryset = queryset.filter(
                Q(veiculo__placa__icontains=buscar) |
                Q(cliente__nome__icontains=buscar) |
                Q(cliente__empresa__icontains=buscar) |
                Q(vaga__codigo__icontains=buscar)
            )
        return queryset.order_by('-data_chegada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar'] = self.request.GET.get('buscar', '')
        return context


class EstadiaChegadaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'estadias.add_estadia'
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = "Dados da chegada cadastrados com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registar Chegada de Veículo"
        return context

    def enviar_email(self, estadia):
        cliente = estadia.cliente
        recipient = [estadia.cliente.email]
        if cliente.tipo_cliente == 'PF':
            nome_cliente = cliente.nome
        else:
            nome_cliente = f"{cliente.nome} - {getattr(cliente, 'empresa', '')}"
        dados = {
            'cliente': nome_cliente,
            'horario': estadia.data_chegada,
            'placa': getattr(estadia.veiculo, 'placa', ''),
            'modelo': getattr(estadia.veiculo, 'modelo', ''),
            'funcionario': getattr(estadia.funcionario, 'nome', ''),
        }
        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)
        try:
            send_mail(
                subject='GESTO - System Parking',
                message=texto_email,
                from_email='piovesannatanael@gmail.com',
                recipient_list=recipient,
                html_message=html_email,
                fail_silently=False
            )
            return True
        except Exception:
            logger.exception("Erro ao enviar email para %s (estadia id=%s): %s", recipient,
                             getattr(estadia, 'pk', '<novo>'),)

            return False

    def form_valid(self, form):

        estadia = form.save(commit=False)
        if estadia.veiculo:
            estadia.plano = estadia.veiculo.plano
        estadia.save()
        self.object = estadia
        self.enviar_email(self.object)
        return super().form_valid(form)


class EstadiaChegadaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'estadias.change_estadia'
    model = Estadia
    form_class = EstadiaChegadaForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = "Dados da chegada atualizados com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Dados da Chegada"
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)



class EstadiaSaidaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'estadias.encerrar_estadia'
    model = Estadia
    form_class = EstadiaSaidaForm
    template_name = 'estadia_saida.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registrar Saída de Veículo"
        return context

    def calcular_duracao_em_horas(self):
        if not self.data_saida:
            return 1
        duracao = self.data_saida - self.data_chegada
        horas = duracao.total_seconds() / 3600
        if horas <= 0:
            return 1
        else:
            return horas

    def form_valid(self, form):
        estadia = form.save(commit=False)

        estadia.save()

        if estadia.veiculo.plano and estadia.veiculo.plano.nome == 'Avulso':
            logger.info("Redirecionando para pagamento_avulso")
            return HttpResponseRedirect(
                reverse('pagamentos_avulso:processar_pagamento_avulso', kwargs={'estada_avulso_pk': estadia.pk}))
        else:
            logger.info("Redirecionando para processar_pagamento_modal")
            return HttpResponseRedirect(
                reverse('pagamentos_modal:processar_pagamento_modal', kwargs={'estada_modal_pk': estadia.pk}))



class EstadiaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'estadias.delete_estadia'
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')
    success_message = "Registro da estadia foi apagado com sucesso."

    def post(self, request, *args, **kwargs):
        estada = self.get_object()
        vaga = estada.vaga

        if vaga:
            vaga.status = 'livre'
            vaga.save()
        messages.success(request, f"A estada do veículo {estada.veiculo.placa} foi apagada e a vaga foi liberada.")

        return super().post(request, *args, **kwargs)



class EstadiaFinalizarView(LoginRequiredMixin, TemplateView):
    template_name = 'pagamento_concluido.html'

    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        estadia.finalizada = True
        estadia.save()

        if estadia.vaga:
            estadia.vaga.status = 'livre'
            estadia.vaga.save()


        messages.success(request, "Pagamento confirmado e estadia finalizada com sucesso!")


def relatorio_estadias(request):

    object_list = Estadia.objects.filter(finalizada=True).order_by('data_saida')
    context = {
        'object_list': object_list,
    }

    return render(request, 'registros.html', context)