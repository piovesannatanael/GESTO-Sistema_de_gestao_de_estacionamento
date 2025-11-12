from django import forms
from .models import Plano, Desconto, Extra, Categoria


class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = [ 'nome', 'valor', 'dias_validade','status', 'descricao']

        widgets = {'dias_validade': forms.NumberInput(attrs={'min': 0,'max': 365, 'placeholder': '0 para planos padrão'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        error_messages = {
            'nome': {'required':'O nome do plano é obrigatório ',
                      'unique':'Já existe um plano com esse nome'},
            'valor': {'required': 'O valor base é obrigatório.',},
            'descricao': {'required': 'A descrição do valor extra é obrigatória.', },
            'dias_validade': {
                'min_value': 'Os dias de validade não podem ser negativos.',
                'max_value': 'Os dias de validade não podem exceder 365 dias.',}

        }

        def clean_dias_validade(self):
            dias_validade = self.cleaned_data.get('dias_validade')
            nome_plano = self.cleaned_data.get('nome')

            if nome_plano == 'Personalizado':
                if not dias_validade or dias_validade == 0:
                    raise forms.ValidationError(
                        "Para planos personalizados, é necessário definir os dias de validade."
                    )
                if dias_validade > 365:
                    raise forms.ValidationError(
                        "Os dias de validade não podem exceder 365 dias."
                    )

            elif nome_plano != 'Avulso' and (not dias_validade or dias_validade == 0):
                validades_padrao = {
                    'Diaria': 1,
                    'Semanal': 7,
                    'Mensal': 30,
                }
                dias_validade = validades_padrao.get(nome_plano, 0)

            elif nome_plano == 'Avulso':
                dias_validade = 0

            return dias_validade

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if self.instance and self.instance.pk:
                if self.instance.nome != 'Personalizado' and self.instance.dias_validade > 0:
                    self.fields['dias_validade'].help_text = f'Validade padrão: {self.instance.dias_validade} dias'

                if self.instance.nome == 'Avulso':
                    self.fields['dias_validade'].widget.attrs['readonly'] = True
                    self.fields['dias_validade'].help_text = 'Plano avulso não possui validade.'


class DescontoForm(forms.ModelForm):
    class Meta:
        model = Desconto
        fields = ['nome', 'tipo', 'valor', 'status', 'descricao']
        error_messages = {
            'nome': {'required': 'O nome do desconto é obrigatório.',},
            'tipo': {'required': 'É obrigatório selecionar o tipo de desconto.',},
            'valor': {'required': 'O valor do desconto é obrigatório.',},
            'descricao': {'required': 'A descrição do desconto é obrigatória.', },

        }

class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields = ['nome', 'tipo', 'valor', 'status', 'descricao']
        error_messages = {
            'nome': {'required': 'O nome do adicional é obrigatório.',},
            'tipo': {'required': 'É obrigatório selecionar o tipo de adicional.',},
            'valor': {'required': 'O valor do adicional é obrigatório.',},
            'descricao': {'required': 'A descrição do valor extra é obrigatória.',},
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['cnh', 'valor_hora', 'status']
        error_messages = {
            'cnh': {'required': 'A categoria é obrigatória.'},
            'valor_hora': {'required': 'O valor por hora é obrigatório.'},
        }