from django import forms
from .models import PagamentoModalidade

class PagamentoModalidadeForm(forms.ModelForm):
    class Meta:
        model = PagamentoModalidade
        # O usuário só precisa preencher o método de pagamento
        fields = ['valor_pago', 'metodo']
        widgets = {
            # Torna o campo de valor somente leitura, pois é calculado pelo sistema
            'valor_pago': forms.NumberInput(attrs={'readonly': True}),
        }
