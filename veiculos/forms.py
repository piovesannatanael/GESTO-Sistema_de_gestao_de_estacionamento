from django import forms
from veiculos.models import Veiculo


class VeiculoModelForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

        error_messages = {
            'placa':{'required':'A placa do veiculo é um campo obrigatório',
                     'unique':'Placa já cadastrada'},
            'qtd_rodas':{'required':'Quantidade de rodas do veiculo é obrigatória'},
            'clientepf':{'required':'É obrigatório o nome do cliente'},

        }