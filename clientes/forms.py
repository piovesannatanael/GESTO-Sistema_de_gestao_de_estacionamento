from django import forms
from django.core.exceptions import ValidationError

from clientes.models import  ClientePF, ClientePJ

'''class ClienteModelForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['tipo_pessoa', 'nome', 'cpf', 'data_nascimento', 'cnpj',
            'fone', 'email', 'endereco', 'foto', 'plano' ]
        widgets = {
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório.'},
            'data_nascimento': {'required': 'A data de nascimento do cliente é um campo obrigatório.'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório.'},
            'fone': {'required': 'O telefone do cliente é um campo obrigatório.'},
            'email': {
                'required': 'O email do cliente é um campo obrigatório.',
                'invalid': 'Formato inválido para email. Ex: fulano@dominio.com',
                'unique': 'Este e-mail já está cadastrado.'
            },
            'plano':  {'required': 'O plano usado é um campo obrigatório.'},
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get('tipo_pessoa')
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')

        if tipo_pessoa == 'PF':
            if cnpj:
                cleaned_data['cnpj'] = ''
            if not cpf:
                self.add_error('cpf', ValidationError("CPF é obrigatório para Pessoa Física."))

        elif tipo_pessoa == 'PJ':
            if cpf:
                cleaned_data['cpf'] = ''
            if not cnpj:
                self.add_error('cnpj', ValidationError("CNPJ é obrigatório para Pessoa Jurídica."))

        return cleaned_data
'''
class ClientePFModelForm(forms.ModelForm):
    class Meta:
        model = ClientePF
        fields = ['nome','cpf','data_nascimento', 'endereco', 'fone', 'email', 'foto', 'plano']

        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'cpf': {'required':'O CPF do cliente é um campo obrigatório'},
            'data_nascimento': {'required':'A data de nascimento do cliente é um campo obrigatório'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
            'fone': {'required': 'O telefone do cliente é um campo obrigatório'},
            'email': {'required': 'O email do cliente é um campo obrigatorio',
                      'invalid': 'Formato invalido para email. Ex: de formato valido: fulano@dominio.com',
                      'unique': 'E-mail ja cadastrado'
                      },
            'plano':  {'requred': 'O plano usado é um campo obrigatório'},

        }

class ClientePJModelForm(forms.ModelForm):
    class Meta:
        model = ClientePJ
        fields = ['nome', 'empresa', 'cnpj', 'endereco', 'fone', 'email', 'foto', 'plano']

        error_messages = {
            'nome': {'required': 'O nome do representante da empresa é um campo obrigatório'},
            'empresa': {'required': 'O nome da empresa é um campo obrigatório'},
            'cnpj': {'required': 'O CNPJ da empresa é um campo obrigatório'},
            'endereco': {'required': 'O endereço da empresa é um campo obrigatório'},
            'fone': {'required': 'O telefone da empresa é um campo obrigatório'},
            'email': {'required': 'O email da empresa é um campo obrigatorio',
                      'invalid': 'Formato invalido para email. Ex: de formato valido: fulano@dominio.com',
                      'unique': 'E-mail ja cadastrado'
                      },
            'plano': {'requred': 'O plano usado é um campo obrigatório'},

        }
