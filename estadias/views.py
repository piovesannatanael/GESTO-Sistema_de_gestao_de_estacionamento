from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
        queryset = super().get_queryset().filter(finalizada=False).select_related(
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Dados da Chegada"
        return context


class EstadiaSaidaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'estadias.change_estadia'
    model = Estadia
    form_class = EstadiaSaidaForm
    template_name = 'estadia_saida.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registrar Saída de Veículo"
        return context

    def form_valid(self, form):
        self.object = form.save()

        vaga = self.object.vaga
        if vaga:
            vaga.status = 'livre'
            vaga.save()

        logger.info(f"Plano do veículo: {self.object.veiculo.plano}")

        if self.object.veiculo.plano == 'Avulso':
            logger.info("Redirecionando para pagamento_avulso")
            return HttpResponseRedirect(reverse('pagamentos_avulso:pagamento_avulso', kwargs={'estada_avulso_pk': self.object.pk}))
        else:
            logger.info("Redirecionando para pagamento_modal_processar")
            return HttpResponseRedirect(reverse('pagamentos_modal:pagamento_modal_processar', kwargs={'estada_modal_pk': self.object.pk}))


class EstadiaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'estadias.delete_estadia'
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

    def post(self, request, *args, **kwargs):
        estada = self.get_object()
        vaga = estada.vaga
        response = super().post(request, *args, **kwargs)
        if vaga:
            vaga.status = 'livre'
            vaga.save()
        messages.success(request, f"A estada do veículo {estada.veiculo.placa} foi apagada e a vaga foi liberada.")

        return response

class DashboardView(ListView):
    model = Estadia
    template_name = 'dashboard.html'


