from django.views.generic import TemplateView

from clientes.models import ClienteGeral


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['qtd_clientes'] = ClienteGeral.objects.count()
        # context['qtd_funcionarios'] = Funcionario.objects.count()
        # context['qtd_veiculos'] = Veiculo.objects.count()
        # context['qtd_vagas'] = Vaga.objects.count()
        # context['qtd_estadas'] = Estada.objects.count()
        return context