from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField

from clientes.models import ClienteGeral


class Veiculo(models.Model):
    RODAS_CHOICES = (
        (2, '2 rodas'),
        (3, '3 rodas'),
        (4, '4 rodas ou mais'),
    )
    PLANOS_CHOICES = (
        ('Diaria', 'Diária'),
        ('Avulso', 'Horário Avulso'),
        ('Semanal', 'Semanal'),
        ('Mensal', 'Mensal'),
    )

    placa = models.CharField('Placa', max_length=8, unique=True)
    marca = models.CharField('Marca', max_length=50)
    modelo = models.CharField('Modelo', max_length=50)
    cor = models.CharField('Cor', max_length=30)
    qtd_rodas = models.IntegerField('Quantidade de Rodas', choices=RODAS_CHOICES)
    plano = models.CharField('Plano', max_length=20, choices=PLANOS_CHOICES)
    clientes = models.ManyToManyField(ClienteGeral,verbose_name='Proprietário(s)',related_name='veiculos')
    foto = StdImageField('Foto', upload_to='carros', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = [Upper('placa')]

    def __str__(self):
        return f'{self.placa} ({self.modelo}) ({self.plano})'

