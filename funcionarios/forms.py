from django import forms
from funcionarios.models import Funcionario


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'data_nascimento', 'funcao', 'data_admissao', 'fone', 'email', 'endereco', 'foto']

        error_messages = {
            'nome': {'required': 'O nome do funcionario é um campo obrigatório'},
            'funcao': {'required': 'A função do funcionário é um campo obrigatório'},
            'fone': {'required': 'O telefone do funcionário é um campo obrigatório'},
            'email': {'required': 'O email do funcionário é um campo obrigatorio',
                      'invalid': 'Formato invalido para email. Ex: de formato valido: fulano@dominio.com',
                      'unique': 'E-mail ja cadastrado'
                      },
            'data_admissao': {'required': 'A data de admissão é um campo obrigatório'}

        }
        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XXX.XXX.XXX-XX',
                'pattern': '[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}',
                'title': 'Formato esperado: XXX.XXX.XXX-XX'
            }),
            'fone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XX XXXXXXXXX',
                'pattern': '\\[0-9]{2}\\ [0-9]{9}',
                'title': 'Formato esperado: XX XXXXXXXXX'
            }),
        }

