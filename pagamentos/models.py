from django.db import models
from django.utils import timezone
from estadias.models import Estadia
from decimal import Decimal

# Definição de preços (pode ser movido para settings.py no futuro)
PRECO_HORA_AVULSA = Decimal('15.00')
PRECO_DIARIA = Decimal('50.00')
PRECO_MENSAL = Decimal('300.00')


class Pagamento(models.Model):
    METODO_CHOICES = (
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
    )
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    )

    # Relação um-para-um: cada estada tem exatamente um pagamento associado.
    estada = models.OneToOneField(Estadia, on_delete=models.CASCADE, related_name='pagamento')

    valor_calculado = models.DecimalField('Valor Calculado', max_digits=8, decimal_places=2, null=True, blank=True)
    metodo = models.CharField('Método de Pagamento', max_length=20, choices=METODO_CHOICES, null=True, blank=True)
    data_pagamento = models.DateTimeField('Data e Hora do Pagamento', null=True, blank=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f'Pagamento para {self.estada.veiculo.placa} - R$ {self.valor_calculado}'

    def calcular_valor(self):
        """
        Calcula o valor da estada com base na duração e no plano da estada.
        """
        if not self.estada.data_saida:
            return Decimal('0.00')  # Não calcula se a saída não foi registrada

        # Pega o plano diretamente da estada, que é um registro histórico.
        plano = self.estada.plano
        duracao = self.estada.data_saida - self.estada.data_chegada

        if plano == 'mensal':
            return PRECO_MENSAL

        elif plano == 'diaria':
            # Arredonda para cima: 1 dia e 1 hora contam como 2 dias.
            dias = (duracao.days) + (1 if duracao.seconds > 0 else 0)
            return PRECO_DIARIA * max(1, dias)  # Cobra no mínimo uma diária

        elif plano == 'horario_avulso':
            # Arredonda para cima: 1h e 10min contam como 2 horas.
            horas = (duracao.total_seconds() / 3600)
            horas_arredondadas = int(horas) + (1 if horas % 1 > 0 else 0)
            return PRECO_HORA_AVULSA * max(1, horas_arredondadas)  # Cobra no mínimo uma hora

        return Decimal('0.00')

    def save(self, *args, **kwargs):
        # Se o pagamento foi marcado como 'pago' e a estada ainda não foi finalizada
        if self.status == 'pago' and not self.estada.finalizada:
            if not self.data_pagamento:
                self.data_pagamento = timezone.now()

            # Atualiza e salva a estada. O método save() da estada cuidará de liberar a vaga.
            self.estada.finalizada = True
            self.estada.valor_total = self.valor_calculado
            # Garante que a data de saída seja preenchida se ainda não estiver
            self.estada.data_saida = self.estada.data_saida or self.data_pagamento
            self.estada.save()

        super().save(*args, **kwargs)

