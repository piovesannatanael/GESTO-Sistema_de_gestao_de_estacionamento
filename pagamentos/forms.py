from django import forms
from .models import Pagamento


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['estadia', 'forma', 'valor_total', 'status', 'observacao']
        widgets = {
            'data_pagamento': forms.DateField(),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'estadia': 'Estadia',
            'forma': 'Forma de Pagamento',
            'valor_total': 'Valor Total (R$)',
            'status': 'Status do Pagamento',
            'observacao': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            from django.utils.timezone import localtime, now
            self.initial['data_pagamento'] = localtime(now()).strftime('%Y-%m-%dT%H:%M')