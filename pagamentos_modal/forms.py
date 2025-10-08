from django import forms
from .models import PagamentoModal

class PagamentoModalForm(forms.ModelForm):
    class Meta:
        model = PagamentoModal
        fields = ['plano_contratado', 'metodo', 'data_pagamento']
        widgets = {
            'data_pagamento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }