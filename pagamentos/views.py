from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils import timezone

from estadias.models import Estadia
from valores.models import Desconto, Extra
from .forms import PagamentoForm
from .models import Pagamento



def enviar_recibo_email(estadia, pagamento):

    try:
        if not estadia.cliente or not estadia.cliente.email:
            print("Cliente sem e-mail cadastrado")
            return False

        context = {
            'estadia': estadia,
            'pagamento': pagamento
        }

        html_message = render_to_string('emails/recibo.html', context)
        text_message = render_to_string('emails/texto_recibo.txt', context)

        send_mail(
            subject='Recibo de Pagamento - Estacionamento',
            message=text_message,
            from_email='piovesannatanael@gmail.com',
            recipient_list=[estadia.cliente.email],
            html_message=html_message,
            fail_silently=False
        )
        print(f"E-mail enviado com sucesso para {estadia.cliente.email}")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False


class ProcessarPagamentoView(LoginRequiredMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'controle_pgto/processar_pagamento.html'

    def get_estadia(self):
        estadia_pk = self.kwargs.get('estadia_pk')
        return get_object_or_404(Estadia, pk=estadia_pk)

    def get_initial(self):
        initial = super().get_initial()
        estadia = self.get_estadia()
        initial['estadia'] = estadia
        # initial['valor_total'] = self.calcular_valor_final(estadia)
        return initial

    def form_valid(self, form):
        pagamento = form.save(commit=False)
        estadia = self.get_estadia()
        forma_pagamento = form.cleaned_data['forma']

        resultado_calculo = self.aplicar_regras_negocio(estadia, forma_pagamento,
                                                        self.calcular_valor_avulso(
                                                            estadia) if estadia.veiculo.plano.is_avulso()
                                                        else self.calcular_valor_plano_fixo(estadia))

        valor_final = resultado_calculo['valor_final']

        pagamento.valor_total = valor_final
        pagamento.estadia = estadia
        pagamento.status = 'PENDENTE'
        pagamento.save()

        return redirect(f'pagamentos:{forma_pagamento.lower()}', pagamento_id=pagamento.id)

    def calcular_duracao_horas(self, estadia):
        if not estadia.data_saida:
            return 0

        duracao = estadia.data_saida - estadia.data_chegada
        horas = duracao.total_seconds() / 3600
        return max(horas, 1)

    def calcular_valor_avulso(self, estadia):
        duracao_horas = self.calcular_duracao_horas(estadia)
        valor_hora = float(estadia.veiculo.plano.valor)

        valor_base = duracao_horas * valor_hora

        if hasattr(estadia.veiculo, 'categoria') and estadia.veiculo.categoria:
            percentual_categoria = float(estadia.veiculo.categoria.valor_hora)
            valor_base += valor_base * (percentual_categoria / 100)

        return valor_base

    def aplicar_descontos(self, valor_base, descontos):
        valor_final = valor_base

        for desconto in descontos:
            if desconto.tipo == 'PERCENTUAL':
                valor_final -= valor_base * (float(desconto.valor) / 100)
            else:
                valor_final -= float(desconto.valor)

        return max(valor_final, 0)

    def aplicar_extras(self, valor_base, extras):
        valor_final = valor_base

        for extra in extras:
            if extra.tipo == 'PERCENTUAL':
                valor_final += valor_base * (float(extra.valor) / 100)
            else:
                valor_final += float(extra.valor)

        return valor_final

    def calcular_valor_plano_fixo(self, estadia):
        valor_base = float(estadia.veiculo.plano.valor)

        if hasattr(estadia.veiculo, 'categoria') and estadia.veiculo.categoria:
            percentual_categoria = float(estadia.veiculo.categoria.valor_hora)
            valor_base += valor_base * (percentual_categoria / 100)

        return valor_base

    def calcular_valor_final(self, estadia):

        if estadia.veiculo.plano.is_avulso():
            valor_base = self.calcular_valor_avulso(estadia)
        else:
            valor_base = self.calcular_valor_plano_fixo(estadia)

        valor_apos_regras = valor_base

        descontos_gerais = Desconto.objects.filter(status=True)

        valor_com_descontos = self.aplicar_descontos(valor_apos_regras, descontos_gerais)

        extras = Extra.objects.filter(status=True)
        valor_final = self.aplicar_extras(valor_com_descontos, extras)

        return round(valor_final, 2)

    def calcular_data_validade(self, estadia):
        if estadia.veiculo.plano.is_avulso():
            return None

        data_base = timezone.now().date()
        return estadia.veiculo.plano.calcular_validade(data_base)

    def get_descontos_aplicados(self, estadia):
        descontos = Desconto.objects.filter(status=True)
        descontos_info = []

        valor_base = self.calcular_valor_avulso(estadia) if estadia.veiculo.plano.is_avulso() else float(
            estadia.veiculo.plano.valor)

        for desconto in descontos:
            if desconto.tipo == 'PERCENTUAL':
                valor_desconto = valor_base * (float(desconto.valor) / 100)
                descontos_info.append({
                    'nome': desconto.nome,
                    'valor': f"-R$ {valor_desconto:.2f} ({desconto.valor}%)"
                })
            else:
                descontos_info.append({
                    'nome': desconto.nome,
                    'valor': f"-R$ {desconto.valor}"
                })

        return descontos_info

    def get_extras_aplicados(self, estadia):
        extras = Extra.objects.filter(status=True)
        extras_info = []

        valor_base = self.calcular_valor_avulso(estadia) if estadia.veiculo.plano.is_avulso() else float(
            estadia.veiculo.plano.valor)

        for extra in extras:
            if extra.tipo == 'PERCENTUAL':
                valor_extra = valor_base * (float(extra.valor) / 100)
                extras_info.append({
                    'nome': extra.nome,
                    'valor': f"+R$ {valor_extra:.2f} ({extra.valor}%)"
                })
            else:
                extras_info.append({
                    'nome': extra.nome,
                    'valor': f"+R$ {extra.valor}"
                })

        return extras_info

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estadia = self.get_estadia()
        plano = estadia.veiculo.plano

        valor_base = self.calcular_valor_avulso(estadia) if plano.is_avulso() else self.calcular_valor_plano_fixo(
            estadia)
        valor_final = self.calcular_valor_final(estadia)
        duracao_horas = self.calcular_duracao_horas(estadia) if plano.is_avulso() else None

        regras_possiveis = self.get_regras_possiveis(estadia)

        context.update({
            'estadia': estadia,
            'veiculo': estadia.veiculo,
            'plano': plano,
            'tipo_pagamento': 'avulso' if plano.is_avulso() else 'plano',
            'valor_base': valor_base,
            'valor_final': valor_final,
            'custo_base': valor_final,
            'data_validade': self.calcular_data_validade(estadia),
            'duracao_horas': duracao_horas,
            'descontos_aplicados': self.get_descontos_aplicados(estadia),
            'extras_aplicados': self.get_extras_aplicados(estadia),
            'categoria': getattr(estadia.veiculo, 'categoria', None),
            'regras_possiveis': regras_possiveis,
        })
        return context

    def get_regras_possiveis(self, estadia):
        from funcionarios.models import Funcionario

        regras_possiveis = []

        try:
            if Funcionario.objects.filter(cpf=estadia.cliente.cpf).exists():
                regras_possiveis.append({
                    'tipo': 'DESCONTO',
                    'nome': 'Desconto Funcionário',
                    'descricao': '20% de desconto para funcionários',
                    'valor': '20%'
                })
        except:
            pass

        duracao_horas = self.calcular_duracao_horas(estadia)
        if duracao_horas > 12:
            regras_possiveis.append({
                'tipo': 'MULTA',
                'nome': 'Multa Tempo Excedido',
                'descricao': f'50% de multa - estadia de {duracao_horas:.1f}h',
                'valor': '50%'
            })

        regras_possiveis.append({
            'tipo': 'DESCONTO',
            'nome': 'Desconto PIX/Dinheiro',
            'descricao': '15% de desconto para pagamentos em PIX ou Dinheiro',
            'valor': '15%'
        })

        return regras_possiveis

    def aplicar_regras_negocio(self, estadia, forma_pagamento, valor_base):

        valor_final = valor_base
        regras_aplicadas = []

        from funcionarios.models import Funcionario
        try:
            if Funcionario.objects.filter(cpf=estadia.cliente.cpf).exists():
                desconto = valor_base * 0.20
                valor_final -= desconto
                regras_aplicadas.append({
                    'tipo': 'DESCONTO',
                    'nome': 'Desconto Funcionário',
                    'valor': desconto
                })
        except:
            pass

        if estadia.veiculo.plano.is_avulso():
            duracao_horas = self.calcular_duracao_horas(estadia)
            if duracao_horas > 12:
                multa = valor_base * 0.50
                valor_final += multa
                regras_aplicadas.append({
                    'tipo': 'MULTA',
                    'nome': 'Multa Tempo Excedido',
                    'valor': multa
                })

        if forma_pagamento in ['PIX', 'DINHEIRO']:
            desconto = valor_base * 0.15
            valor_final -= desconto
            regras_aplicadas.append({
                'tipo': 'DESCONTO',
                'nome': 'Desconto PIX/Dinheiro',
                'valor': desconto
            })

        return {
            'valor_final': max(valor_final, 0),
            'regras_aplicadas': regras_aplicadas
        }

    def atualizar_plano_veiculo(self, veiculo, estadia):
        if not veiculo.plano.is_avulso():
            data_base = estadia.data_saida.date() if estadia.data_saida else timezone.now().date()
            veiculo.atualizar_vencimento_plano(data_base)


class PagamentoDinheiroView(View):
    template_name = 'formas_pgto/dinheiro.html'

    def get(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        context = {
            'pagamento': pagamento,
            'estadia': pagamento.estadia
        }
        return render(request, self.template_name, context)

    def post(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return self.finalizar_pagamento(request, pagamento)

    def finalizar_pagamento(self, request, pagamento):
        estadia = pagamento.estadia

        if estadia:
            # Finalizar estadia
            estadia.finalizada = True
            estadia.valor_total = pagamento.valor_total
            estadia.data_saida = timezone.now()
            estadia.save()

            # Liberar vaga
            if estadia.vaga:
                estadia.vaga.status = 'livre'
                estadia.vaga.save()

            # Atualizar plano se necessário
            if not estadia.veiculo.plano.is_avulso():
                data_base = estadia.data_saida.date() if estadia.data_saida else timezone.now().date()
                estadia.veiculo.atualizar_vencimento_plano(data_base)

            # Enviar e-mail apenas se tiver estadia
            enviar_recibo_email(estadia, pagamento)

            # atualizar o pagamento
        pagamento.status = 'PAGO'
        pagamento.data_pagamento = timezone.now()
        pagamento.save()

        messages.success(request, f'Pagamento de R$ {pagamento.valor_total} processado com sucesso!')
        return redirect('pagamentos:pagamento_concluido', pagamento_id=pagamento.id)


class PagamentoPixView(View):
    template_name = 'formas_pgto/pix.html'

    def get(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        context = {
            'pagamento': pagamento,
            'estadia': pagamento.estadia
        }
        return render(request, self.template_name, context)

    def post(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return PagamentoDinheiroView().finalizar_pagamento(request, pagamento)



class PagamentoCreditoView(View):
    template_name = 'formas_pgto/credito.html'

    def get(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        context = {
            'pagamento': pagamento,
            'estadia': pagamento.estadia
        }
        return render(request, self.template_name, context)

    def post(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return PagamentoDinheiroView().finalizar_pagamento(request, pagamento)


class PagamentoDebitoView(View):
    template_name = 'formas_pgto/debito.html'

    def get(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        context = {
            'pagamento': pagamento,
            'estadia': pagamento.estadia
        }
        return render(request, self.template_name, context)

    def post(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return PagamentoDinheiroView().finalizar_pagamento(request, pagamento)


class PagamentoConcluidoDetalhesView(View):

    def get(self, request, pagamento_id):
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        context = {
            'pagamento': pagamento,
            'estadia': pagamento.estadia
        }
        return render(request, 'controle_pgto/pagamento_concluido.html', context)


class SaidaPlanoValidoView(View):
    template_name = 'formas_pgto/plano_valido.html'

    def get(self, request, estadia_id):
        estadia = get_object_or_404(Estadia, id=estadia_id)

        if not estadia.veiculo.plano_esta_valido:
            return redirect('pagamentos:processar_pagamento', estadia_id=estadia_id)

        context = {
            'estadia': estadia,
            'veiculo': estadia.veiculo,
            'plano': estadia.veiculo.plano
        }
        return render(request, self.template_name, context)

    def post(self, request, estadia_id):
        estadia = get_object_or_404(Estadia, id=estadia_id)

        estadia.finalizada = True
        estadia.data_saida = timezone.now()
        estadia.valor_total = 0
        estadia.save()

        if estadia.vaga:
            estadia.vaga.status = 'livre'
            estadia.vaga.save()

        messages.success(request,
                         f'Saída registrada com sucesso! Plano válido até {estadia.veiculo.data_vencimento_plano.strftime("%d/%m/%Y")}')
        return redirect('estadias')


class PagamentosView(LoginRequiredMixin, ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(
                Q(estadia__id__icontains=buscar) |
                Q(forma__icontains=buscar) |
                Q(valor_total__icontains=buscar) |
                Q(estadia__veiculo__placa__icontains=buscar) |
                Q(estadia__cliente__nome__icontains=buscar)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar'] = self.request.GET.get('buscar', '')
        return context


class PagamentoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'controle_pgto/pagamento_form.html'
    success_url = reverse_lazy('pagamentos:pagamentos')
    success_message = 'Pagamento cadastrado com sucesso!'
    print("Cadastrando pagamento")

    def form_valid(self, form):
        pagamento = form.save(commit=False)

        pagamento.status = 'PENDENTE'
        pagamento.save()

        forma_pagamento = form.cleaned_data.get('forma')
        if forma_pagamento:
            return redirect(f'pagamentos:{forma_pagamento.lower()}', pagamento_id=pagamento.id)
        else:
            return redirect('pagamentos:pagamentos')

class PagamentoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'controle_pgto/pagamento_form.html'
    success_url = reverse_lazy('pagamentos:pagamentos')
    success_message = 'Pagamento alterado com sucesso!'

    def form_valid(self, form):
        pagamento = form.save(commit=False)

        if pagamento.status != 'PAGO':
            pagamento.status = 'PENDENTE'

        pagamento.save()

        forma_pagamento = form.cleaned_data.get('forma')
        if forma_pagamento and pagamento.status != 'PAGO':
            return redirect(f'pagamentos:{forma_pagamento.lower()}', pagamento_id=pagamento.id)
        else:
            return redirect('pagamentos:pagamentos')


class PagamentoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pagamento
    template_name = 'controle_pgto/pagamento_apagar.html'
    success_url = reverse_lazy('pagamentos:pagamentos')
    success_message = 'Pagamento excluído com sucesso!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)