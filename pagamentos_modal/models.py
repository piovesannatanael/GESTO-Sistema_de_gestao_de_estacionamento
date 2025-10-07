from django.db import models
from decimal import Decimal
from estadias.models import Estadia
from funcionarios.models import Funcionario


PRECOS_PLANOS = {
    'diaria': Decimal('20.00'),
    'semanal': Decimal('50.00'),
    'mensal': Decimal('200.00'),
}


class PagamentoModal(models.Model):
    PLANO_CHOICES = (
        ('diaria', 'Diária'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
    )
    METODO_CHOICES = (
        ('PIX', 'PIX'),
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO', 'Cartão'),
    )
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    )

    estadia = models.OneToOneField(
        Estadia,
        on_delete=models.PROTECT,
        related_name='pagamento_modal'
    )

    plano_contratado = models.CharField('Plano Contratado', max_length=20, choices=PLANO_CHOICES)
    metodo = models.CharField('Método de Pagamento', max_length=20, choices=METODO_CHOICES)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='PENDENTE')

    valor_bruto = models.DecimalField('Valor Bruto', max_digits=8, decimal_places=2, null=True, blank=True)
    desconto_aplicado = models.DecimalField('Desconto Aplicado', max_digits=8, decimal_places=2,
                                            default=Decimal('0.00'))
    valor_final = models.DecimalField('Valor Final', max_digits=8, decimal_places=2, null=True, blank=True)

    data_pagamento = models.DateTimeField('Data do Pagamento', null=True, blank=True)

    class Meta:
        verbose_name = 'Pagamento de Modalidade'
        verbose_name_plural = 'Pagamentos de Modalidades'

    def __str__(self):
        return f'Pagamento de {self.get_plano_contratado_display()} para {self.estadia.veiculo.placa}'

    def calcular_valores(self):
        preco_base = PRECOS_PLANOS.get(self.plano_contratado, Decimal('0.00'))

        veiculo = self.estadia.veiculo
        acrescimo = Decimal('0.00')
        qtd_rodas_str = str(getattr(veiculo, 'qtd_rodas', '0'))

        if qtd_rodas_str == '2':
            acrescimo = preco_base * Decimal('0.02')
        elif qtd_rodas_str in ['3', '4 ou mais']:
            acrescimo = preco_base * Decimal('0.03')

        valor_bruto = preco_base + acrescimo

        desconto_funcionario = Decimal('0.00')
        desconto_pagamento = Decimal('0.00')

        if self.estadia.cliente and hasattr(self.estadia.cliente, 'cpf'):
            if Funcionario.objects.filter(cpf=self.estadia.cliente.cpf).exists():
                desconto_funcionario = valor_bruto * Decimal('0.20')

        if self.metodo in ['PIX', 'DINHEIRO']:
            desconto_pagamento = valor_bruto * Decimal('0.15')

        maior_desconto = max(desconto_funcionario, desconto_pagamento)
        valor_final = valor_bruto - maior_desconto

        return {
            'valor_bruto': round(valor_bruto, 2),
            'desconto': round(maior_desconto, 2),
            'valor_final': round(valor_final, 2),
        }

    def save(self, *args, **kwargs):
        valores = self.calcular_valores()
        self.valor_bruto = valores['valor_bruto']
        self.desconto_aplicado = valores['desconto']
        self.valor_final = valores['valor_final']

        if self.status == 'PAGO':
            self.estadia.valor_total = self.valor_final
            self.estadia.finalizada = True
            self.estadia.save()

        super().save(*args, **kwargs)

