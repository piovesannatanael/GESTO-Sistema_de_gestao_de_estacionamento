# pagamentos_avulso/forms.py
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

    # campo somente leitura exibido no form (não faz parte do model)
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
        # NÃO inclua 'valor_calculado' aqui — liste apenas campos reais do model
        fields = ['metodo']  # ajuste se quiser persistir mais campos do model diretamente

    def __init__(self, *args, instance=None, estadia=None, **kwargs):
        """
        Pode passar instance (PagamentoAvulso) ou estadia (Estadia) para calcular o valor.
        """
        super().__init__(*args, instance=instance, **kwargs)

        initial_val = None
        # se veio uma instance (objeto PagamentoAvulso), use a propriedade valor_calculado do model
        if instance is not None:
            initial_val = getattr(instance, 'valor_calculado', None)

        # se foi passada uma estadia, monte temporariamente para calcular (não salva nada)
        if initial_val is None and estadia is not None:
            # import local para evitar possíveis import cycles em tempo de import do módulo
            from .models import PagamentoAvulso as _PagoTemp
            temp = _PagoTemp(estadia=estadia, metodo='PIX')
            initial_val = getattr(temp, 'valor_calculado', None)

        if initial_val is None:
            initial_val = Decimal('0.00')

        self.fields['valor_calculado'].initial = initial_val


# alias para compatibilidade com outros módulos que importam PagamentoForm
PagamentoForm = PagamentoAvulsoForm
