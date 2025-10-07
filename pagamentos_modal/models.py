# pagamentos_modal/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta

# imports locais para evitar circularidade em tempo de import, se necessário
# from estadias.models import Estadia
# from funcionarios.models import Funcionario

# --- PREÇOS BASE PARA CADA MODALIDADE ---
PRECOS_PLANOS = {
    'diaria': Decimal('15.00'),
    'semanal': Decimal('50.00'),
    'mensal': Decimal('200.00'),
}


def _to_decimal(value):
    try:
        return Decimal(value)
    except Exception:
        return Decimal('0.00')


class PagamentoModal(models.Model):
    """
    Modelo para gerenciar pagamentos de estadias por planos
    (diária, semanal, mensal).
    """
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

    estadia = models.OneToOneField(
        'estadias.Estadia',
        on_delete=models.CASCADE,
        related_name='pagamento_modal'
    )
    plano_contratado = models.CharField(
        'Plano Contratado',
        max_length=10,
        choices=PLANO_CHOICES
    )
    metodo = models.CharField('Método de Pagamento', max_length=20, choices=METODO_CHOICES)

    valor_bruto = models.DecimalField(
        'Valor Bruto (sem descontos)',
        max_digits=8,
        decimal_places=2,
        null=True, blank=True
    )
    desconto_aplicado = models.DecimalField(
        'Desconto Aplicado',
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_final = models.DecimalField(
        'Valor Final (a pagar)',
        max_digits=8,
        decimal_places=2,
        null=True, blank=True
    )
    data_pagamento = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Pagamento por Modalidade'
        verbose_name_plural = 'Pagamentos por Modalidade'

    def __str__(self):
        placa = '??'
        try:
            placa = self.estadia.veiculo.placa
        except Exception:
            pass
        return f'Pagamento ({self.get_plano_contratado_display()}) para {placa}'

    def calcular_valores(self):
        """
        Calcula o valor final do pagamento com base no plano contratado,
        aplicando acréscimos e descontos.
        Retorna dict com Decimal quantizado com 2 casas.
        """
        # segurança: se estadia/veiculo ausente, retorna zeros
        if not getattr(self, 'estadia', None) or not getattr(self.estadia, 'veiculo', None):
            zero = Decimal('0.00')
            return {'valor_bruto': zero, 'desconto': zero, 'valor_final': zero}

        # --- 1. Obter Preço Base do Plano ---
        preco_base = PRECOS_PLANOS.get(self.plano_contratado, Decimal('0.00'))
        preco_base = _to_decimal(preco_base)

        # --- 2. Aplicar Acréscimo com base na Categoria do Veículo ---
        veiculo = self.estadia.veiculo
        acrescimo = Decimal('0.00')

        # tenta transformar em int; se falhar, assume 0
        qtd_rodas = getattr(veiculo, 'qtd_rodas', None)
        try:
            qtd_rodas_int = int(qtd_rodas)
        except Exception:
            qtd_rodas_int = 0

        if qtd_rodas_int == 2:
            acrescimo = preco_base * Decimal('0.02')  # Acréscimo de 2%
        elif qtd_rodas_int >= 3:
            acrescimo = preco_base * Decimal('0.03')  # Acréscimo de 3%

        valor_bruto = preco_base + acrescimo

        # NOTA: A regra de multa por +12h não se aplica a planos de preço fixo.

        # --- 3. Calcular e Aplicar o Maior Desconto Disponível ---
        desconto_funcionario = Decimal('0.00')
        desconto_pagamento = Decimal('0.00')

        # import local para checar funcionário (evita circular import em top-level)
        try:
            from funcionarios.models import Funcionario
            cliente = getattr(self.estadia, 'cliente', None)
            if cliente and hasattr(cliente, 'cpf'):
                is_funcionario = Funcionario.objects.filter(cpf=cliente.cpf).exists()
                if is_funcionario:
                    desconto_funcionario = valor_bruto * Decimal('0.20')
        except Exception:
            # se módulo de funcionários não estiver disponível, ignoramos
            desconto_funcionario = Decimal('0.00')

        if (self.metodo or '').upper() in ['PIX', 'DINHEIRO']:
            desconto_pagamento = valor_bruto * Decimal('0.15')

        maior_desconto = max(desconto_funcionario, desconto_pagamento)
        valor_final = valor_bruto - maior_desconto

        # quantize para 2 casas, arredondamento padrão HALF_UP
        q = Decimal('0.01')
        valor_bruto_q = valor_bruto.quantize(q, rounding=ROUND_HALF_UP)
        maior_desconto_q = maior_desconto.quantize(q, rounding=ROUND_HALF_UP)
        valor_final_q = valor_final.quantize(q, rounding=ROUND_HALF_UP)

        return {
            'valor_bruto': valor_bruto_q,
            'desconto': maior_desconto_q,
            'valor_final': valor_final_q,
        }

    # compatibilidade com views/forms que chamam calcular_valor()
    def calcular_valor(self):
        return self.calcular_valores()

    @property
    def valor_pago(self):
        """Alias read-only para compatibilidade com código que espera 'valor_pago'."""
        if self.valor_final is not None:
            return self.valor_final
        return self.calcular_valores().get('valor_final', Decimal('0.00'))

    def save(self, *args, **kwargs):
        # Recalcula valores quando necessário:
        # - no create (sem pk)
        # - ou se valor_final está em branco
        # - ou se plano/metodo mudou (heurística simples)
        recompute = False
        if not self.pk:
            recompute = True
        if self.valor_final in (None, ''):
            recompute = True

        if recompute:
            valores = self.calcular_valores()
            self.valor_bruto = valores['valor_bruto']
            self.desconto_aplicado = valores['desconto']
            self.valor_final = valores['valor_final']

        # Atualiza a estadia relacionada de maneira segura
        try:
            if self.valor_final is not None and getattr(self, 'estadia', None):
                self.estadia.valor_total = self.valor_final
                self.estadia.finalizada = True
                self.estadia.save()
        except Exception:
            # não queremos quebrar save por conta de problemas na estadia
            pass

        super().save(*args, **kwargs)
