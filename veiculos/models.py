from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Upper
from django.db import models

from clientes.models import Pessoa, ClientePF


class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=8, help_text='Placa do veiculo', unique=True)
    marca = models.CharField('Marca', max_length=15, help_text='Marca do veiculo')
    modelo = models.CharField('Modelo', max_length=15, help_text='Modelo do veiculo')
    cor = models.CharField('Cor', max_length=15, help_text='Cor do veiculo')
    qtd_rodas = models.DecimalField('Quantidade de rodas', max_digits=2, decimal_places=0, help_text='Quantidade de rodas do veículo')
    cliente = models.ManyToManyField(Pessoa, related_name="veiculos")
    # object_id = models.PositiveIntegerField()
#     cliente = GenericForeignKey('content_type', 'object_id')
    class Meta:
        verbose_name = 'Veiculo'
        verbose_name_plural = 'Veiculos'
        ordering = [Upper('placa')]



    def __str__(self):
        return self.placa



