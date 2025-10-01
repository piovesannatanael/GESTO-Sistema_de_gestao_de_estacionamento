from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Upper
from django.db import models


from django.db import models
from django.db.models.functions import Upper
from clientes.models import ClienteGeral  # Importe o modelo unificado


class Veiculo(models.Model):
    RODAS_CHOICES = (
        (2, '2 rodas'),
        (3, '3 rodas'),
        (4, '4 rodas ou mais'),
    )
    PLANOS_CHOICES = (
        ('diaria', 'Diária'),
        ('horario_avulso', 'Horário Avulso'),
        ('mensal', 'Mensal'),
    )

    placa = models.CharField('Placa', max_length=8, unique=True)
    marca = models.CharField('Marca', max_length=50)
    modelo = models.CharField('Modelo', max_length=50)
    cor = models.CharField('Cor', max_length=30)
    qtd_rodas = models.IntegerField('Quantidade de Rodas', choices=RODAS_CHOICES)
    plano = models.CharField('Plano', max_length=20, choices=PLANOS_CHOICES)
    clientes = models.ManyToManyField(ClienteGeral,verbose_name='Proprietário(s)',related_name='veiculos')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = [Upper('placa')]

    def __str__(self):
        return f'{self.placa} ({self.clientes})'


    # class Meta:
    #     ordering = ['placa']
    #
    # def __str__(self):
    #     @property
    #     def cliente_nome(self):
    #         c = self.cliente
    #         if not c:
    #             return ''
    #         return getattr(c, 'nome', None) or getattr(c, 'empresa', None) or str(c)






    # cliente_pf = models.ForeignKey(
    #     ClientePF,
    #     verbose_name='Cliente PF',
    #     related_name="veiculos",
    #     on_delete=models.CASCADE,
    #     null=True, blank=True  # Permite que este campo seja nulo
    # )
    # cliente_pj = models.ForeignKey(
    #     ClientePJ,
    #     verbose_name='Cliente PJ',
    #     related_name="veiculos",
    #     on_delete=models.CASCADE,
    #     null=True, blank=True  # Permite que este campo seja nulo
    # )
    #
    # class Meta:
    #     verbose_name = 'Veiculo'
    #     verbose_name_plural = 'Veiculos'
    #     ordering = [Upper('placa')]
    #
    # constraints = [
    #     # Garante que ou cliente_pf ou cliente_pj seja preenchido, mas não ambos.
    #     CheckConstraint(
    #         check=(
    #                 Q(cliente_pf__isnull=False, cliente_pj__isnull=True) |
    #                 Q(cliente_pf__isnull=True, cliente_pj__isnull=False)
    #         ),
    #         name='apenas_um_tipo_de_cliente'
    #     )
    # ]
    #
    # @property
    # def cliente(self):
    #     return self.cliente_pf or self.cliente_pj
    #
    # def __str__(self):
    #     return self.placa

    # def __str__(self):
    #     return self.placa



