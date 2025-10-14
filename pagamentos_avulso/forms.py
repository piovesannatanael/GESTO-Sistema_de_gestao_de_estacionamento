from django import forms
from valores.models import Desconto, Extra

class PagamentoAvulsoForm(forms.Form):
    PAGAMENTO_CHOICES = (
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CREDITO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
    )

    desconto = forms.ModelChoiceField(queryset=Desconto.objects.filter(status=True),required=False,label='Aplicar Desconto',
        empty_label="Nenhum desconto")
    extra = forms.ModelChoiceField(queryset=Extra.objects.filter(status=True), required=False,label='Adicionar Extra',
        empty_label="Nenhum extra")
    forma_pagamento = forms.ChoiceField(choices=PAGAMENTO_CHOICES,required=True,label='Forma de Pagamento',widget=forms.RadioSelect )