# pagamentos_modal/forms.py
from decimal import Decimal
from django import forms
from .models import PagamentoModal

class PagamentoModalForm(forms.ModelForm):
    """
    Form para pagamentos de modalidade.
    - 'valor_pago' é um campo apenas de exibição (disabled) que mostra o valor_final calculado.
    - Meta.fields lista somente campos reais do model.
    """
    valor_pago = forms.DecimalField(
        label='Valor a pagar (R$)',
        max_digits=12,
        decimal_places=2,
        required=False,
        disabled=True,
        initial=Decimal('0.00')
    )

    class Meta:
        model = PagamentoModal
        # Somente campos que realmente existem no model.
        # Ajuste se quiser que o form salve mais campos do model.
        fields = ['plano_contratado', 'metodo', 'data_pagamento']

    def __init__(self, *args, instance=None, modalidade=None, **kwargs):
        """
        Aceita `instance` (PagamentoModal) ou `modalidade` para calcular o valor mostrado.
        """
        super().__init__(*args, instance=instance, **kwargs)

        initial_val = None

        # Se houver instance do PagamentoModal, usamos o valor_final do model
        if instance is not None:
            initial_val = getattr(instance, 'valor_final', None)

        # Se não, se for passada a modalidade (ou outro objeto) tentamos inferir preço
        if initial_val is None and modalidade is not None:
            # exemplo: modalidade.preco ou outra lógica — ajuste conforme seu model/modalidade
            initial_val = getattr(modalidade, 'preco', None) or getattr(modalidade, 'valor', None)

        if initial_val is None:
            initial_val = Decimal('0.00')

        # garante Decimal
        try:
            initial_val = Decimal(initial_val)
        except Exception:
            initial_val = Decimal('0.00')

        self.fields['valor_pago'].initial = initial_val


# alias para compatibilidade com importações que esperam PagamentoForm
PagamentoForm = PagamentoModalForm
