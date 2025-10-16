from django import forms

from pagamento.models import Pagamento
from valores.models import Extra, Desconto


class PagamentoForm(forms.ModelForm):
    desconto = forms.ModelChoiceField(
        queryset=Desconto.objects.filter(status=True),
        required=False,
        label='Aplicar Desconto',
        empty_label="Nenhum desconto"
    )
    extra = forms.ModelChoiceField(
        queryset=Extra.objects.filter(status=True),
        required=False,
        label='Adicionar Extra',
        empty_label="Nenhum extra"
    )
    forma_pagamento = forms.ChoiceField(choices=Pagamento.PAGAMENTO_CHOICES,required=True,label='Forma de Pagamento',widget=forms.RadioSelect,initial="DINHEIRO"
    )