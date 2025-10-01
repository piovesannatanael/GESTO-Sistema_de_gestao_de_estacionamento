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





# from django import forms
# from django.core.exceptions import ValidationError
#
# from clientes.models import ClientePF, ClientePJ
#
# class ClientePFModelForm(forms.ModelForm):
#     class Meta:
#         model = ClientePF
#         fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'fone', 'email', 'foto']
#         widgets = {
#             'nome': forms.TextInput(attrs={'class': 'form-control'}),
#             'cpf': forms.TextInput(attrs={'class': 'form-control'}),
#             'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'endereco': forms.TextInput(attrs={'class': 'form-control'}),
#             'fone': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
#         error_messages = {
#             'nome': {'required': 'O nome do cliente é um campo obrigatório'},
#             'cpf': {'required': 'O CPF do cliente é um campo obrigatório'},
#             'data_nascimento': {'required': 'A data de nascimento do cliente é um campo obrigatório'},
#             'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
#             'fone': {'required': 'O telefone do cliente é um campo obrigatório'},
#             'email': {
#                 'required': 'O email do cliente é um campo obrigatório',
#                 'invalid': 'Formato inválido para email. Ex: fulano@dominio.com',
#                 'unique': 'E-mail já cadastrado'
#             },
#         }
#
#     def clean(self):
#         cleaned = super().clean()
#         cpf = cleaned.get('cpf')
#         if not cpf:
#             self.add_error('cpf', ValidationError("CPF é obrigatório para Pessoa Física."))
#         cleaned['cnpj'] = None
#         cleaned['empresa'] = None
#         return cleaned
#
#     def save(self, commit=True):
#         self.instance.tipo_cliente = 'PF'
#         return super().save(commit=commit)
#
#
# class ClientePJModelForm(forms.ModelForm):
#     class Meta:
#         model = ClientePJ
#         fields = ['nome', 'empresa', 'cnpj', 'endereco', 'fone', 'email', 'foto']
#         widgets = {
#             'nome': forms.TextInput(attrs={'class': 'form-control'}),
#             'empresa': forms.TextInput(attrs={'class': 'form-control'}),
#             'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
#             'endereco': forms.TextInput(attrs={'class': 'form-control'}),
#             'fone': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
#         error_messages = {
#             'nome': {'required': 'O nome do representante da empresa é um campo obrigatório'},
#             'empresa': {'required': 'O nome da empresa é um campo obrigatório'},
#             'cnpj': {'required': 'O CNPJ da empresa é um campo obrigatório'},
#             'endereco': {'required': 'O endereço da empresa é um campo obrigatório'},
#             'fone': {'required': 'O telefone da empresa é um campo obrigatório'},
#             'email': {
#                 'required': 'O email da empresa é um campo obrigatório',
#                 'invalid': 'Formato inválido para email. Ex: fulano@dominio.com',
#                 'unique': 'E-mail já cadastrado'
#             },
#         }
#
#     def clean(self):
#         cleaned = super().clean()
#         cnpj = cleaned.get('cnpj')
#         if not cnpj:
#             self.add_error('cnpj', ValidationError("CNPJ é obrigatório para Pessoa Jurídica."))
#         # Garantir que campos de PF fiquem None (não '')
#         cleaned['cpf'] = None
#         cleaned['data_nascimento'] = None
#         return cleaned
#
#     def save(self, commit=True):
#         # garante que tipo_cliente seja PJ no registro pai ClienteGeral
#         self.instance.tipo_cliente = 'PJ'
#         return super().save(commit=commit)
