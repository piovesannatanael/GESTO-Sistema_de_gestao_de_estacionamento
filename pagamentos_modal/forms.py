from django import forms
from .models import PagamentoModalidade

class PagamentoModalidadeForm(forms.ModelForm):
    class Meta:
        model = PagamentoModalidade
        fields = ['valor_pago', 'metodo']
        widgets = {
            'valor_pago': forms.NumberInput(attrs={'readonly': True}),
        }
