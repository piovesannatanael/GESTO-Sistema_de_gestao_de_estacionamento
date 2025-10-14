from django import forms
from .models import Veiculo

class VeiculoModelForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

        widgets = {
            'clientes': forms.CheckboxSelectMultiple(),
        }
        error_messages = {
            'placa':{'required':'A placa do veículo é obrigatória',
                     'unique':'Placa já cadastrada'},
            'marca':{'required':'A marca do veiculo é obrigatorio'},
            'modelo':{'required':'O modelo do veiculo é obrigatorio'},
            'foto':{'required':'A foto do veículo é obrigatória para futura identificação'}
        }
