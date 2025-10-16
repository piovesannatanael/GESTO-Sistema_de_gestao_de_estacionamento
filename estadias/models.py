from django.db import models
from django.utils import timezone
from veiculos.models import Veiculo
from clientes.models import ClienteGeral
from funcionarios.models import Funcionario
from vagas.models import Vaga


class Estadia(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    cliente = models.ForeignKey(ClienteGeral, on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True, blank=True)
    data_chegada = models.DateTimeField(default=timezone.now)
    data_saida = models.DateTimeField(null=True, blank=True)
    finalizada = models.BooleanField(default=True)
    valor_total = models.DecimalField('Valor Total', max_digits=8, decimal_places=2, default=0, null=True, blank=True)

    class Meta:
        permissions = (('encerrar_estadia','Permite fazer o encerramento de uma estadia'),)
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['-data_chegada']

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'

    def calcular_duracao_em_horas(self):
        if not self.data_saida:
            return 1
        duracao = self.data_saida - self.data_chegada
        horas = duracao.total_seconds() / 3600
        if horas <= 0:
            return 1
        else:
            return horas

    def save(self, *args, **kwargs):
        vaga_original = None
        if self.pk:
            try:
                vaga_original = Estadia.objects.get(pk=self.pk).vaga
            except Estadia.DoesNotExist:
                pass
        super().save(*args, **kwargs)

        if self.vaga:
            if self.finalizada:
                self.vaga.status = 'livre'
            else:
                self.vaga.status = 'ocupada'
            self.vaga.save()

        if vaga_original and vaga_original != self.vaga:
            vaga_original.status = 'livre'
            vaga_original.save()

