from django.db import models
from django.db.models.functions import Upper

from clientes.models import PessoaFisica


class Funcionario(PessoaFisica):
    cpf = models.CharField('CPF ', max_length=14, unique=True, null=True, blank=True)
    funcao = models.CharField('Função', max_length=35, help_text='Função na empresa')
    data_admissao = models.DateField('Admissão', help_text='Data de admissão na empresa')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = [Upper('nome')]


    def __str__(self):
        return f"{self.nome} - {self.funcao}"