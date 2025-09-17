from clientes import forms
from funcionarios.models import Funcionario


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao', 'fone', 'email', 'data_admissao', 'foto']
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