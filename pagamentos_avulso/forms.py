from django import forms
from .models import PagamentoAvulso
from decimal import Decimal

class PagamentoAvulsoForm(forms.ModelForm):
    desconto = forms.DecimalField(
        label='Desconto (R$)',
        required=False,
        min_value=0,
        initial=Decimal('0.00'),
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )
    valor_adicional = forms.DecimalField(
        label='Valor Adicional (R$)',
        required=False,
        min_value=0,
        initial=Decimal('0.00'),
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )

    valor_calculado = forms.DecimalField(
        label='Valor calculado (R$)',
        max_digits=10,
        decimal_places=2,
        required=False,
        disabled=True,
        initial=Decimal('0.00')
    )

    class Meta:
        model = PagamentoAvulso
        fields = ['metodo']

    def __init__(self, *args, instance=None, estadia=None, **kwargs):

        super().__init__(*args, instance=instance, **kwargs)

        initial_val = None
        if instance is not None:
            initial_val = getattr(instance, 'valor_calculado', None)

        if initial_val is None and estadia is not None:
            from .models import PagamentoAvulso as _PagoTemp
            temp = _PagoTemp(estadia=estadia, metodo='PIX')
            initial_val = getattr(temp, 'valor_calculado', None)

        if initial_val is None:
            initial_val = Decimal('0.00')

        self.fields['valor_calculado'].initial = initial_val


PagamentoForm = PagamentoAvulsoForm
