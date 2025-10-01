# veiculos/forms.py

from django import forms
from .models import Veiculo  # Importa o seu *novo* modelo Veiculo


class VeiculoModelForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

        widgets = {
            'clientes': forms.CheckboxSelectMultiple(),
        }