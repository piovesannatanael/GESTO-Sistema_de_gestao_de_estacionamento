from django.db import models
from funcionarios.models import Funcionario
from clientes.models import ClienteGeral
from veiculos.models import Veiculo



class Valores(models.Model):
    plano = models.CharField('Plano', max_length=20, choices=Veiculo.PLANOS_CHOICES, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(ClienteGeral, on_delete=models.SET_NULL, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        permissions = (('alterar_valores','Permite atualizar os valores da tabela'),)
        verbose_name = 'Valor'
        verbose_name_plural = 'Valores'

    def __str__(self):
        return self.valor_total