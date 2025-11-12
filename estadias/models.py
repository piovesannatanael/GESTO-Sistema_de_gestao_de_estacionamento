from django.db import models
from django.utils import timezone

class Estadia(models.Model):
    veiculo = models.ForeignKey('veiculos.Veiculo', on_delete=models.PROTECT)
    cliente = models.ForeignKey('clientes.ClienteGeral', on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey('funcionarios.Funcionario', on_delete=models.SET_NULL, null=True, blank=True)
    vaga = models.ForeignKey('vagas.Vaga', on_delete=models.SET_NULL, null=True, blank=True)
    data_chegada = models.DateTimeField(default=timezone.now)
    data_saida = models.DateTimeField(null=True, blank=True)
    finalizada = models.BooleanField(default=False)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['-data_chegada']

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'

