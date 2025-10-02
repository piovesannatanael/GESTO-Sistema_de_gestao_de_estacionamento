from django.views.generic import TemplateView
from clientes.models import ClienteGeral
from estadias.models import Estadia
from funcionarios.models import Funcionario
from vagas.models import Vaga
from veiculos.models import Veiculo


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['qtd_clientes'] = ClienteGeral.objects.count()
        context['qtd_funcionarios'] = Funcionario.objects.count()
        context['qtd_veiculos'] = Veiculo.objects.count()
        context['qtd_vagas'] = Vaga.objects.count()
        context['qtd_estadias'] = Estadia.objects.count()
        return context