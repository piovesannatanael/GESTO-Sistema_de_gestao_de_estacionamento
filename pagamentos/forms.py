from django import forms
from .models import Pagamento
from valores.models import Desconto, Extra


class PagamentoForm(forms.ModelForm):
    desconto = forms.ModelChoiceField(queryset=Desconto.objects.filter(status=True),
        required=False,label='Aplicar Desconto',empty_label="Nenhum desconto")
    extra = forms.ModelChoiceField(queryset=Extra.objects.filter(status=True),
        required=False,label='Adicionar Extra', empty_label="Nenhum extra")

    class Meta:
        model = Pagamento
        fields = ['estadia', 'forma', 'status', 'observacao']
        widgets = {
            'estadia': forms.HiddenInput(),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'forma': forms.RadioSelect(),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'valor_total': 'Valor Total',
            'forma': 'Forma de Pagamento',
            'status': 'Status do Pagamento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estadia'].required = False

        if not self.instance.pk:
            self.fields['status'].initial = 'PENDENTE'