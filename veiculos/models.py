from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Upper
from django.db import models

from clientes.models import Pessoa, ClientePF, ClientePJ


class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=8, help_text='Placa do veiculo', unique=True)
    marca = models.CharField('Marca', max_length=15, help_text='Marca do veiculo')
    modelo = models.CharField('Modelo', max_length=15, help_text='Modelo do veiculo')
    cor = models.CharField('Cor', max_length=15, help_text='Cor do veiculo')
    qtd_rodas = models.DecimalField('Quantidade de rodas', max_digits=2, decimal_places=0, help_text='Quantidade de rodas do veículo')


    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    cliente = GenericForeignKey('content_type', 'object_id')

    # Duas ForeignKeys, uma para cada tipo de cliente. Ambas podem ser nulas.
    cliente_pf = models.ForeignKey(
        ClientePF,
        verbose_name='Cliente PF',
        related_name="veiculos",
        on_delete=models.CASCADE,
        null=True, blank=True  # Permite que este campo seja nulo
    )
    cliente_pj = models.ForeignKey(
        ClientePJ,
        verbose_name='Cliente PJ',
        related_name="veiculos",
        on_delete=models.CASCADE,
        null=True, blank=True  # Permite que este campo seja nulo
    )

    class Meta:
        verbose_name = 'Veiculo'
        verbose_name_plural = 'Veiculos'
        ordering = [Upper('placa')]

    constraints = [
        # Garante que ou cliente_pf ou cliente_pj seja preenchido, mas não ambos.
        CheckConstraint(
            check=(
                    Q(cliente_pf__isnull=False, cliente_pj__isnull=True) |
                    Q(cliente_pf__isnull=True, cliente_pj__isnull=False)
            ),
            name='apenas_um_tipo_de_cliente'
        )
    ]

    @property
    def cliente(self):
        return self.cliente_pf or self.cliente_pj

    def __str__(self):
        return self.placa

    # def __str__(self):
    #     return self.placa



