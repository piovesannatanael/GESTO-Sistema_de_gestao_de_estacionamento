from django.db import models
from veiculos.models import Veiculo


class Plano(models.Model):

    plano = models.CharField('Plano', max_length=20, choices=Veiculo.PLANOS_CHOICES, null=True, blank=True)
    valor = models.DecimalField('Valor Base (R$)', max_digits=8, decimal_places=2)
    status = models.BooleanField('Ativo', default=True, help_text='Marque para ativar o plano')

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f"{self.plano} - R$ {self.valor}"


class Desconto(models.Model):
    DESCONTO_CHOICES = (
        ('PERCENTUAL', 'Percentual (%)'),
        ('FIXO', 'Valor Fixo (R$)'),
    )

    nome = models.CharField('Nome do desconto', max_length=100, help_text='Ex: Desconto para funcionário')
    tipo = models.CharField('Tipo de desconto', max_length=20, choices=DESCONTO_CHOICES)
    valor = models.DecimalField('Valor do desconto', max_digits=8, decimal_places=2, help_text='Somente números')
    ativo = models.BooleanField('Ativo', default=True, help_text='Marque para ativar este desconto')

    class Meta:
        verbose_name = 'Desconto'
        verbose_name_plural = 'Descontos'

    def __str__(self):
        if self.tipo == 'PERCENTUAL':
            return f"{self.nome} ({self.valor}%)"
        return f"{self.nome} (R$ {self.valor})"



class Extra(models.Model):
    EXTRA_CHOICES = (
        ('PERCENTUAL', 'Percentual (%)'),
        ('FIXO', 'Valor Fixo (R$)'),
    )

    nome = models.CharField('Nome do adicional', max_length=100, help_text='Ex: ')
    tipo = models.CharField('Tipo do adicional', max_length=20, choices=EXTRA_CHOICES)
    valor = models.DecimalField('Valor a adicionar (R$)', max_digits=8, decimal_places=2, help_text='Somente números')
    ativo = models.BooleanField('Ativo', default=True, help_text='Marque para ativar este valor extra')

    class Meta:
        verbose_name = 'Valor Extra'
        verbose_name_plural = 'Valores Extras'

    def __str__(self):
        return f"{self.nome} (+ R$ {self.valor})"