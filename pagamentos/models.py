from django.db import models
from django.utils import timezone
from estadias.models import Estadia


class Pagamento(models.Model):
    PAGAMENTO_CHOICES = (
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CREDITO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
    )
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    )

    data_pagamento = models.DateTimeField('Data do Pagamento', default=timezone.now)
    forma = models.CharField('Forma de Pagamento', max_length=20, choices=PAGAMENTO_CHOICES, default='DINHEIRO')
    valor_total = models.DecimalField('Valor Total', max_digits=8, decimal_places=2, default=0)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE, related_name='pagamentos')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PAGO')
    observacao = models.TextField('Observação', blank=True, null=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f'Pagamento #{self.id} - Estadia #{self.estadia.id} - R$ {self.valor_total}'

    def save(self, *args, **kwargs):
        if not self.valor_total and self.estadia:
            self.valor_total = self.estadia.valor_total or 0
        super().save(*args, **kwargs)