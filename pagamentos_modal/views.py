from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from modalidades.models import Modalidade
from .forms import PagamentoModalidadeForm


class PagarModalidadeView(View):
    template_name = 'pagamentos_modal/pagamento_modalidade.html'

    def get(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        # Preenche o formulário com o valor a ser pago (com multa, se houver)
        form = PagamentoModalidadeForm(initial={'valor_pago': modalidade.valor_com_multa})

        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)

    def post(self, request, modalidade_pk):
        modalidade = get_object_or_404(Modalidade, pk=modalidade_pk)
        form = PagamentoModalidadeForm(request.POST)

        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.modalidade = modalidade
            pagamento.save()

            # Redireciona de volta para a lista de modalidades após o sucesso
            return redirect('modalidades:modalidade_list')

        # Se o formulário for inválido, renderiza a página novamente com os erros
        context = {
            'form': form,
            'modalidade': modalidade,
        }
        return render(request, self.template_name, context)
