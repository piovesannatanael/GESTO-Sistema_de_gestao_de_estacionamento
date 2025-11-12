from django import forms
from .models import Vaga


class VagaModelForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['codigo', 'status']

        error_messages = {
            'codigo': {
                'required': 'O código da vaga é um campo obrigatório.',
                'unique': 'Uma vaga com este código já está cadastrada!',
            },
            'status': {
                'required': 'A seleção do status é um campo obrigatório.',
            },
        }