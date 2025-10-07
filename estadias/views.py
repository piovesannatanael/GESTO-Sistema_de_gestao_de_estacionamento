from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

from .models import Estadia
from .forms import EstadiaChegadaForm, EstadiaSaidaForm


class EstadiaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'estadias.view_estadia'
    model = Estadia
    template_name = 'estadias.html'
    context_object_name = 'object_list'
    paginate_by = 9

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

    def form_valid(self, form):
        # Primeiro, copia o plano do veículo para a estada antes de guardar
        veiculo = form.cleaned_data.get('veiculo')
        if veiculo:
            form.instance.plano = veiculo.plano

        # Guarda o objeto e continua o fluxo normal da CreateView
        response = super().form_valid(form)

        # --- LÓGICA DE ENVIO DE EMAIL ADAPTADA E ADICIONADA ---
        # self.object agora contém a estada que acabámos de criar.
        estada = self.object

        try:
            # 1. Prepara os dados para o template do e-mail
            dados = {
                'cliente': estada.cliente,
                'veiculo': estada.veiculo,
                'horario': estada.data_chegada,
                'funcionario': estada.funcionario,
            }

            # 2. Renderiza o template HTML do e-mail e cria uma versão em texto simples
            html_email = render_to_string('emails/texto_email.html', dados)
            texto_email = strip_tags(html_email)

            # 3. Envia o e-mail
            send_mail(
                subject='GESTO - Confirmação de Chegada do Veículo',
                message=texto_email,
                from_email='nao-responda@gesto.com.br',  # Substitua pelo seu e-mail de envio
                recipient_list=[estada.cliente.email],
                html_message=html_email,
                fail_silently=False  # Levanta um erro se o envio falhar
            )
            messages.success(self.request, "Estada registada e e-mail de confirmação enviado com sucesso!")
        except Exception as e:
            # Adiciona uma mensagem de erro se o e-mail não puder ser enviado
            messages.error(self.request, f"A estada foi registada, mas o e-mail de confirmação falhou: {e}")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Registar Chegada de Veículo"
        return context


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
        context["titulo"] = "Registar Saída de Veículo"
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pagamento_processar', kwargs={'estada_pk': self.object.pk})


class EstadiaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'estadias.delete_estadia'
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')

