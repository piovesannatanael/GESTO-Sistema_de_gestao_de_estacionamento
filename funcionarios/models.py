from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField

from clientes.models import PessoaFisica


class Funcionario(PessoaFisica):
    nome = models.CharField('Nome',max_length=50, help_text='Nome completo')
    funcao = models.CharField('Função', max_length=35, help_text='Função na empresa')
    fone = models.CharField('Fone',max_length=15, help_text='Numero de telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='E-mail', unique=True)
    data_admissao = models.CharField('Admissão', help_text='Data de admissão na empresa')
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = [Upper('nome')]


def __str__(self):
    return super().nome