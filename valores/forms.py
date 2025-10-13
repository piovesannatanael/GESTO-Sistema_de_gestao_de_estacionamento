from django import forms
from .models import Plano, Desconto, Extra


class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = [ 'plano', 'valor', 'status', 'descricao']

        error_messages = {
            'plano': {'required':'É obrigatório selecionar o plano',
                      'unique':'Já existe um plano com esse nome'},
            'valor': {'required': 'O valor base é obrigatório.',},
            'descricao': {'required': 'A descrição do valor extra é obrigatória.', },

        }


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