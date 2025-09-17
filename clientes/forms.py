from django import forms

from clientes.models import ClientePF, ClientePJ


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