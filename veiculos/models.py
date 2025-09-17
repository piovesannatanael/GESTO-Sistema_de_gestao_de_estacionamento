from django.db.models.functions import Upper
from django.db import models
import clientes.models


class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=8, help_text='Placa do veiculo', unique=True)
    marca = models.CharField('Marca', max_length=15, help_text='Marca do veiculo')
    modelo = models.CharField('Modelo', max_length=15, help_text='Modelo do veiculo')
    cor = models.CharField('Cor', max_length=15, help_text='Cor do veiculo')
    qtd_rodas = models.DecimalField('Quantidade de rodas', max_digits=2, decimal_places=0, help_text='Quantidade de rodas do veículo')
    cliente = models.ForeignKey(clientes.models.ClientePF, verbose_name='Cliente PF', on_delete=models.PROTECT(), help_text="Nome do cliente",
                                related_name='clientepf')

    class Meta:
        verbose_name = 'Veiculo'
        verbose_name_plural = 'Veiculos'
        ordering = [Upper('placa')]

    def __str__(self):
        return self.nome