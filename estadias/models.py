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
    vaga = models.ForeignKey(Vaga, on_delete=models.PROTECT)
    plano = models.CharField('Plano', max_length=20, choices=Veiculo.PLANOS_CHOICES, null=True, blank=True)


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
        original_vaga = None
        if self.pk:
            try:
                original_vaga = Estadia.objects.get(pk=self.pk).vaga
            except Estadia.DoesNotExist:
                pass
        if self.finalizada:
            self.vaga.status = 'livre'
        else:
            self.vaga.status = 'ocupada'
        self.vaga.save()
        if original_vaga and original_vaga != self.vaga:
            original_vaga.status = 'livre'
            original_vaga.save()

        super().save(*args, **kwargs)

