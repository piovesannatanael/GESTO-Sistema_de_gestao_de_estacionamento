from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from veiculos.models import Veiculo
from clientes.models import ClienteGeral
from funcionarios.models import Funcionario
from vagas.models import Vaga


class Estadia(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    cliente = models.ForeignKey(ClienteGeral, on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.PROTECT)

    data_chegada = models.DateTimeField(default=timezone.now)
    data_saida = models.DateTimeField(null=True, blank=True)
    finalizada = models.BooleanField(default=False)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['-data_chegada']

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'

    def save(self, *args, **kwargs):
        if not self.pk and not self.finalizada:
            estada_ativa_existente = Estadia.objects.filter(veiculo=self.veiculo, finalizada=False).exists()
            if estada_ativa_existente:
                raise ValidationError(
                    f'O veículo de placa {self.veiculo.placa} já possui uma estada ativa.'
                )

        if self.finalizada:
            self.vaga.status = 'livre'
        else:
            self.vaga.status = 'ocupada'
        self.vaga.save()

        super().save(*args, **kwargs)
