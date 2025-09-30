from itertools import chain

from django import forms
from django.contrib.contenttypes.models import ContentType

from clientes.models import ClientePJ, ClientePF
from veiculos.models import Veiculo


class VeiculoModelForm(forms.ModelForm):
    cliente_choice = forms.ChoiceField(label='Proprietario', required=True)

    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'cor', 'qtd_rodas', 'cliente_choice']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clientes = chain(
            [(f"clientepf_{pf.id}", f"{pf.nome} (PF)") for pf in ClientePF.objects.all()],
            [(f"clientepj_{pj.id}", f"{pj.empresa} (PJ)") for pj in ClientePJ.objects.all()],
        )
        self.fields['cliente_choice'].choices = list(clientes)

        if self.instance and self.instance.pk and self.instance.cliente:
            cliente_obj = self.instance.cliente
            content_type = ContentType.objects.get_for_model(cliente_obj)
            if content_type.model == 'clientepf':
                self.fields['cliente_choice'].initial = f'clientepf_{cliente_obj.id}'
            else:
                self.fields['cliente_choice'].initial = f'clientepj_{cliente_obj.id}'


        # super().__init__(*args, **kwargs)
        #
        # clientes_pf = ClientePF.objects.all()
        # clientes_pj = ClientePJ.objects.all()
        # choices = [('', '---------')]
        #
        # for cliente in clientes_pf:
        #     ct = ContentType.objects.get_for_model(cliente)
        #     choices.append((f'{ct.id}-{cliente.id}', f'{cliente.nome} (PF)'))
        #
        # for cliente in clientes_pj:
        #     ct = ContentType.objects.get_for_model(cliente)
        #     choices.append((f'{ct.id}-{cliente.id}', f'{cliente.nome} (PJ)'))
        #
        # self.fields['cliente'].choices = choices
        #
        # # mantem o cliente na edição
        # if self.instance and self.instance.pk and self.instance.cliente:
        #     ct = ContentType.objects.get_for_model(self.instance.cliente)
        #     self.fields['cliente'].initial = f'{ct.id}-{self.instance.cliente.id}'

