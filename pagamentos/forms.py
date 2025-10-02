from django import forms
from .models import Pagamento


class PagamentoForm(forms.ModelForm):

    desconto = forms.DecimalField(
        label='Desconto (R$)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )
    valor_adicional = forms.DecimalField(
        label='Valor Adicional (R$)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )

    class Meta:
        model = Pagamento
        fields = ['valor_calculado', 'metodo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor_calculado'].disabled = True

