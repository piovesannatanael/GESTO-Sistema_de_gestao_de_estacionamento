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
    )

    data = models.DateTimeField(default=timezone.now)
    forma = models.CharField(choices=PAGAMENTO_CHOICES,required=True ,label='Forma de Pagamento')
    valor_total = models.FloatField(max_digits=8, decimal_places=2, null=True, blank=True)
    estadia = models.OneToOneField(Estadia, on_delete=models.CASCADE, related_name='pagamento')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDENTE')


    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data']

    def __str__(self):
        return f'{self.estadia.id} - {self.valor_total}'