from django import forms
from django.utils.timezone import localtime, now  # CORREÇÃO: Garante que 'localtime' e 'now' estão importados
from django.core.exceptions import ValidationError
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

        vagas_livres = Vaga.objects.filter(status="livre")
        # Garante que, na edição, a vaga atual do veículo apareça na lista de opções
        if self.instance and self.instance.pk and self.instance.vaga:
            vagas_livres = vagas_livres | Vaga.objects.filter(pk=self.instance.vaga.pk)
        self.fields['vaga'].queryset = vagas_livres.distinct()

        self.fields['veiculo'].queryset = Veiculo.objects.order_by('placa')
        self.fields['cliente'].queryset = ClienteGeral.objects.order_by('nome', 'empresa')
        self.fields['funcionario'].queryset = Funcionario.objects.order_by('nome')

    def clean_veiculo(self):
        veiculo = self.cleaned_data.get('veiculo')
        if veiculo:
            query = Estadia.objects.filter(veiculo=veiculo, finalizada=False)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise ValidationError(
                    f'Este veículo (placa {veiculo.placa}) já se encontra no pátio em outra estada ativa.'
                )
        return veiculo


class EstadiaSaidaForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = ['data_saida']
        widgets = {
            'data_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche o campo 'data_saida' com o horário local atual por padrão
        if not self.instance.data_saida:
            # CORREÇÃO: Usa localtime() para converter a hora UTC para o fuso horário local (ex: São Paulo)
            self.initial['data_saida'] = localtime(now()).strftime('%Y-%m-%dT%H:%M')

