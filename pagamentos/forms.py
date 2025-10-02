from django import forms
from .models import Pagamento
from decimal import Decimal

class ProcessarPagamentoForm(forms.Form):
    # Pega as opções de método do modelo Pagamento
    metodo = forms.ChoiceField(
        choices=Pagamento.METODO_CHOICES,
        widget=forms.RadioSelect, # Mostra como botões de rádio, mais amigável
        label="Método de Pagamento"
    )
    valor_calculado = forms.DecimalField(
        label="Valor Calculado (R$)",
        disabled=True,
        required=False
    )
    desconto = forms.DecimalField(
        label="Desconto (R$)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )
    valor_adicional = forms.DecimalField(
        label="Valor Adicional (R$)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )

    def clean_desconto(self):
        # Garante que o desconto não seja maior que o valor calculado
        desconto = self.cleaned_data.get('desconto') or Decimal('0.00')
        valor_calculado = self.initial.get('valor_calculado')
        if valor_calculado and desconto > valor_calculado:
            raise forms.ValidationError("O desconto não pode ser maior que o valor calculado.")
        return desconto
