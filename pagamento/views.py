from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from funcionarios.forms import FuncionarioModelForm
from pagamento.forms import PagamentoForm
from pagamento.models import Pagamento


class PagamentosView(ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 1

    def get_queryset(self):
        qs = super().get_queryset()
        buscar = self.request.GET.get('buscar')

        if buscar:
            qs = qs.filter(
                Q(data__icontains=buscar) |
                Q(forma__icontains=buscar)
            )
        return qs

class PagamentoCreateView(SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'pagamentos_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento cadastrado com sucesso!'

class PagamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'pagamentos_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento alterado com sucesso!'

class PagamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Pagamento
    template_name = 'pagamentos_apagar.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento excluido com sucesso!'


class PagamentoCreateView(View):
    form_class = PagamentoForm
    template_name = 'pagamentos/pagamento_processar.html'

    def get(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        # Lógica de cálculo do valor base
        custo_base = 0.0
        duracao_horas = estadia.calcular_duracao_em_horas()
        try:
            preco_categoria = Categoria.objects.get(cnh=estadia.veiculo.categoria_cnh, status=True)
            custo_base = duracao_horas * float(preco_categoria.valor_hora)
        except Categoria.DoesNotExist:
            messages.error(request,
                           f"Não há um preço ativo para a categoria '{estadia.veiculo.get_categoria_cnh_display()}'.")

        form = self.form_class()
        context = {
            'estadia': estadia,
            'form': form,
            'custo_base': custo_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        estadia_pk = self.kwargs.get('estadia_pk')
        estadia = get_object_or_404(Estadia, pk=estadia_pk)

        form = self.form_class(request.POST)

        # Recalcula o custo base para segurança
        custo_base = 0.0
        duracao_horas = estadia.calcular_duracao_em_horas()
        try:
            preco_categoria = Categoria.objects.get(cnh=estadia.veiculo.categoria_cnh, status=True)
            custo_base = duracao_horas * float(preco_categoria.valor_hora)
        except Categoria.DoesNotExist:
            messages.error(request, "Erro ao calcular o preço base.")
            return redirect('estadias')

        if form.is_valid():
            cleaned_data = form.cleaned_data
            # Lógica completa de cálculo do valor final
            # (incluindo extras, descontos, etc., como fizemos antes)
            # ...
            total_final = custo_base  # Simplificado por enquanto

            # Cria um novo objeto Pagamento PENDENTE
            pagamento, created = Pagamento.objects.get_or_create(
                estadia=estadia,
                defaults={
                    'valor_total': total_final,
                    'forma_pagamento': cleaned_data.get('forma_pagamento'),
                    'status': 'PENDENTE'
                }
            )
            if not created:  # Se o pagamento já existia, atualiza
                pagamento.valor_total = total_final
                pagamento.forma_pagamento = cleaned_data.get('forma_pagamento')
                pagamento.save()

            # Redireciona para a tela de detalhes do pagamento
            return redirect('pagamento_detalhe', pk=pagamento.pk)

        context = {'estadia': estadia, 'form': form, 'custo_base': custo_base}
        return render(request, self.template_name, context)


class PagamentoDetailView(View):
    def get(self, request, *args, **kwargs):
        pagamento_pk = self.kwargs.get('pk')
        pagamento = get_object_or_404(Pagamento, pk=pagamento_pk)

        # Determina qual template de pagamento final mostrar
        template_name = f'pagamentos/pagamento_{pagamento.forma_pagamento.lower()}.html'

        context = {'pagamento': pagamento}
        return render(request, template_name, context)


class PagamentoConfirmarView(View):
    def post(self, request, *args, **kwargs):
        pagamento_pk = self.kwargs.get('pk')
        pagamento = get_object_or_404(Pagamento, pk=pagamento_pk)

        # Atualiza o status do pagamento
        pagamento.status = 'PAGO'
        pagamento.data_pagamento = timezone.now()
        pagamento.save()

        # Finaliza a estadia
        estadia = pagamento.estadia
        estadia.finalizada = True
        estadia.save()

        # Libera a vaga
        if estadia.vaga:
            estadia.vaga.status = 'livre'
            estadia.vaga.save()

        # Envia o e-mail de recibo (lógica a ser implementada)
        messages.success(request, "Pagamento confirmado e estadia finalizada com sucesso!")

        return render(request, 'pagamentos/pagamento_concluido.html', {'pagamento': pagamento})
