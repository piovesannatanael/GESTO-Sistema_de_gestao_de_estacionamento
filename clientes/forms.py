from django import forms

from clientes.models import ClienteGeral


class ClienteGeralModelForm(forms.ModelForm):
    class Meta:
        model = ClienteGeral

        fields = [
            'tipo_cliente', 'nome', 'fone', 'email', 'endereco', 'foto',
            'cpf', 'data_nascimento', 'empresa', 'cnpj'
        ]
        widgets = {
                    'nome': forms.TextInput(attrs={'class': 'form-control'}),
                    'cpf': forms.TextInput(attrs={'class': 'form-control'}),
                    'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                    'endereco': forms.TextInput(attrs={'class': 'form-control'}),
                    'fone': forms.TextInput(attrs={'class': 'form-control'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                }
        error_messages = {
                    'nome': {'required': 'O nome do cliente é um campo obrigatório'},
                    'cpf': {'required': 'O CPF do cliente é um campo obrigatório'},
                    'data_nascimento': {'required': 'A data de nascimento do cliente é um campo obrigatório'},
                    'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
                    'fone': {'required': 'O telefone do cliente é um campo obrigatório'},
                    'email': {
                        'required': 'O email do cliente é um campo obrigatório',
                        'invalid': 'Formato inválido para email. Ex: fulano@dominio.com',
                        'unique': 'E-mail já cadastrado'
                    },
                }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tipo_cliente'].disabled = True

