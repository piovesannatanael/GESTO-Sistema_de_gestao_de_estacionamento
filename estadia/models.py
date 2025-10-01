# estada/models.py

from django.db import models
from veiculos.models import Veiculo
from clientes.models import ClienteGeral
from funcionarios.models import Funcionario
from vagas.models import Vaga


class Estada(models.Model):
    # --- RELACIONAMENTOS (SEUS REQUISITOS) ---

    # ForeignKey: Uma Estada está ligada a UM Veículo.
    veiculo = models.ForeignKey(
        Veiculo,
        verbose_name='Veículo',
        on_delete=models.PROTECT  # Impede que um veículo seja apagado se tiver uma estada ativa
    )

    # ForeignKey: A Estada é registrada por UM Funcionário.
    funcionario = models.ForeignKey(
        Funcionario,
        verbose_name='Funcionário Responsável',
        on_delete=models.SET_NULL,  # Se o funcionário for apagado, o registro da estada permanece
        null=True,
        blank=True
    )

    # ForeignKey: A Estada está associada a UM Cliente específico (dentre os donos do veículo).
    cliente = models.ForeignKey(
        ClienteGeral,
        verbose_name='Cliente',
        on_delete=models.SET_NULL,  # Se o cliente for apagado, o registro permanece
        null=True,
        blank=True
    )

    # ForeignKey: A Estada ocupa UMA Vaga.
    vaga = models.ForeignKey(
        Vaga,
        verbose_name='Vaga',
        on_delete=models.PROTECT  # Impede que uma vaga seja apagada se tiver estadas associadas
    )

    # --- CONTROLE DE TEMPO E STATUS (ESSENCIAL) ---

    # Data e hora da chegada (seu requisito)
    data_chegada = models.DateTimeField('Data e Hora da Chegada', auto_now_add=True)

    # Data e hora da saída (essencial para o cálculo)
    data_saida = models.DateTimeField('Data e Hora da Saída', null=True, blank=True)

    # Status para saber se a estada está em andamento ou já foi finalizada
    finalizada = models.BooleanField('Finalizada', default=False)

    # --- VALORES (ESSENCIAL) ---
    valor_total = models.DecimalField('Valor Total', max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Estada'
        verbose_name_plural = 'Estadas'
        ordering = ['-data_chegada']  # Ordena pelas mais recentes primeiro

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'

    def save(self, *args, **kwargs):
        # Lógica para ocupar a vaga na criação da estada
        if not self.pk:  # Se é um objeto novo (criação)
            self.vaga.ocupada = True
            self.vaga.save()

        # Lógica para desocupar a vaga na finalização da estada
        if self.finalizada and self.data_saida is not None:
            self.vaga.ocupada = False
            self.vaga.save()

        super(Estada, self).save(*args, **kwargs)