from django import forms
from valores.models import Desconto, Extra
from estadias.models import Estadia

class PagamentoModalForm(forms.Form):
    desconto = forms.ModelChoiceField(queryset=Desconto.objects.filter(status=True),required=False,label='Aplicar Desconto',empty_label="Nenhum desconto")
    extra = forms.ModelChoiceField(queryset=Extra.objects.filter(status=True),required=False,label='Adicionar Extra',empty_label="Nenhum extra")
    forma_pagamento = forms.ChoiceField(choices=Estadia.PAGAMENTO_CHOICES,required=True,label='Forma de Pagamento',widget=forms.RadioSelect,initial="PIX")