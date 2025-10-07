# pagamentos_modal/forms.py
from decimal import Decimal
from django import forms
from .models import PagamentoModal

class PagamentoModalForm(forms.ModelForm):
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
        fields = ['plano_contratado', 'metodo', 'data_pagamento']

    def __init__(self, *args, instance=None, modalidade=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)

        initial_val = None

        if instance is not None:
            initial_val = getattr(instance, 'valor_final', None)

        if initial_val is None and modalidade is not None:
            initial_val = getattr(modalidade, 'preco', None) or getattr(modalidade, 'valor', None)

        if initial_val is None:
            initial_val = Decimal('0.00')

        try:
            initial_val = Decimal(initial_val)
        except Exception:
            initial_val = Decimal('0.00')

        self.fields['valor_pago'].initial = initial_val


PagamentoForm = PagamentoModalForm
