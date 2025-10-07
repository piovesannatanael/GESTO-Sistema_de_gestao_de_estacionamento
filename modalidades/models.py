from django.db import models
from django.utils import timezone
from veiculos.models import Veiculo
from decimal import Decimal
from datetime import timedelta

PRECO_DIARIA = Decimal('50.00')
PRECO_SEMANAL = Decimal('100.00')
PRECO_MENSAL = Decimal('300.00')


class Modalidade(models.Model):
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='modalidade')
    ultimo_pagamento = models.DateTimeField(null=True, blank=True)
    valido_ate = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Modalidade de Plano'
        verbose_name_plural = 'Modalidades de Planos'

    @property
    def plano(self):
        return self.veiculo.get_plano_display()

    @property
    def valor(self):
        if self.veiculo.plano == 'mensal':
            return PRECO_MENSAL
        if self.veiculo.plano == 'semanal':
            return PRECO_SEMANAL
        if self.veiculo.plano == 'diaria':
            return PRECO_DIARIA
        return Decimal('0.00')

    @property
    def esta_atrasado(self):
        if not self.valido_ate:
            return True
        return timezone.now() > self.valido_ate + timedelta(days=0.5)

    @property
    def valor_com_multa(self):
        valor_base = self.valor
        if self.esta_atrasado:
            multa = valor_base * Decimal('0.10')
            return (valor_base + multa).quantize(Decimal('0.01'))
        return valor_base

    def registrar_pagamento(self):
        self.ultimo_pagamento = timezone.now()
        if self.veiculo.plano == 'mensal':
            self.valido_ate = self.ultimo_pagamento + timedelta(days=30)
        elif self.veiculo.plano == 'semanal':
            self.valido_ate = self.ultimo_pagamento + timedelta(days=7)
        elif self.veiculo.plano == 'diaria':
            self.valido_ate = self.ultimo_pagamento + timedelta(days=1)
        self.save()

    def __str__(self):
        return f'Plano {self.plano} para {self.veiculo.placa}'

