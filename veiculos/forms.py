from django import forms
from clientes.models import Pessoa
from veiculos.models import Veiculo

class VeiculoModelForm(forms.ModelForm):
    cliente = forms.ModelMultipleChoiceField(
        queryset=Pessoa.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Clientes"
    )

    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'cor', 'qtd_rodas', 'cliente']



    # def __init__(self, *args, **kwargs): buscar pj e pf e fazer a junção apra o input
    #     super().__init__(*args, **kwargs)

    #     clientes_pf = ClientePF.objects.all()
    #     clientes_pj = ClientePJ.objects.all()
    #     choices = [('', '---------')]
    #
    #     for cliente in clientes_pf:
    #         ct = ContentType.objects.get_for_model(cliente)
    #         choices.append((f'{ct.id}-{cliente.id}', f'{cliente.nome} (PF)'))
    #
    #     for cliente in clientes_pj:
    #         ct = ContentType.objects.get_for_model(cliente)
    #         choices.append((f'{ct.id}-{cliente.id}', f'{cliente.nome} (PJ)'))
    #
    #     self.fields['cliente'].choices = choices

        #     if self.instance and self.instance.pk and self.instance.cliente:
    #         ct = ContentType.objects.get_for_model(self.instance.cliente)
    #         self.fields['cliente'].initial = f'{ct.id}-{self.instance.cliente.id}'
    #
    # def save(self, commit=True):
    #     cliente_data = self.cleaned_data['cliente'].split('-')
    #     content_type_id = int(cliente_data[0])
    #     object_id = int(cliente_data[1])
    #
    #     self.instance.content_type_id = content_type_id
    #     self.instance.object_id = object_id
    #
    #     return super().save(commit)