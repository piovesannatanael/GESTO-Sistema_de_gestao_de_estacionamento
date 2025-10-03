from django.db import models
from django.utils import timezone
from modalidades.models import Modalidade
from pagamentos.models import Pagamento # Reutiliza as choices

class PagamentoModalidade(models.Model):
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name='pagamentos')
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateTimeField(default=timezone.now)
    metodo = models.CharField('Método', max_length=20, choices=Pagamento.METODO_CHOICES)

    class Meta:
        verbose_name = 'Pagamento de Plano'
        verbose_name_plural = 'Pagamentos de Planos'
        ordering = ['-data_pagamento']

    def save(self, *args, **kwargs):
        # Garante que, ao salvar este pagamento, o status da modalidade seja atualizado.
        super().save(*args, **kwargs)
        self.modalidade.registrar_pagamento()


    def __str__(self):
        return f'Pagamento do plano para {self.modalidade.veiculo.placa} - R$ {self.valor_pago}'
