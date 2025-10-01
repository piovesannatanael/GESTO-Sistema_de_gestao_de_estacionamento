from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Estadia
from vagas.models import Vaga
from veiculos.models import Veiculo
from clientes.models import ClienteGeral
from funcionarios.models import Funcionario


class EstadiaChegadaForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = ['veiculo', 'cliente', 'funcionario', 'vaga']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vaga'].queryset = Vaga.objects.filter(status="livre")
        self.fields['veiculo'].queryset = Veiculo.objects.order_by('placa')
        self.fields['cliente'].queryset = ClienteGeral.objects.order_by('nome', 'empresa')
        self.fields['funcionario'].queryset = Funcionario.objects.order_by('nome')

    def clean_veiculo(self):
        veiculo = self.cleaned_data.get('veiculo')
        if veiculo:
            estada_ativa = Estadia.objects.filter(veiculo=veiculo, finalizada=False).exists()
            if estada_ativa:
                raise ValidationError(
                    f'Este veículo (placa {veiculo.placa}) já se encontra no pátio e não pode dar entrada novamente.'
                )
        return veiculo


class EstadiaSaidaForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = ['data_saida', 'finalizada']
        widgets = {
            'data_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.data_saida:
            self.initial['data_saida'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.initial['finalizada'] = True
        self.fields['finalizada'].disabled = True

