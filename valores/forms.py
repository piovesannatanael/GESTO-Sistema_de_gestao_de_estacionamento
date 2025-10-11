from django import forms
from .models import Valores

class ValoresModelForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = ['plano','qtd_rodas','desconto_pag','desconto_func']

        error_messages = {
            'plano': {'required':'É obrigatório selecionar o plano!'},
            'qtd_rodas': {'required':'É obrigatório informar a quantidade de rodas!'},
        }