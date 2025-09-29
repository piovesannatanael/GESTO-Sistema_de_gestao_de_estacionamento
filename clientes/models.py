from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    fone = models.CharField('Fone', max_length=15, help_text='Numero de telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='E-mail', unique=True)
    endereco = models.CharField('Endereço', max_length=300, help_text='Endereço completo')
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = [Upper('nome')]

    def __str__(self):
        return self.nome

class PessoaFisica(Pessoa):
    cpf = models.CharField('CPF', max_length=11, unique=True,null=True, blank=True, help_text='Digite o CPF')
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True, help_text='Data de nascimento')

    class Meta:
        abstract = True

    def __str__(self):
        return self.cpf

class PessoaJuridica(Pessoa):
    empresa = models.CharField('Empresa', max_length=100, help_text='Nome da empresa')
    cnpj = models.DecimalField('CNPJ', max_digits=14, unique=True, decimal_places=0, help_text='Digite o CNPJ da empresa')

    class Meta:
        abstract = True

    def __str__(self):
        return self.empresa


class ClientePF(PessoaFisica):
    PLANOS_OPCOES = (
        ('diaria', 'Diária'),
        ('horario_avulso', 'Horário Avulso'),
        ('mensal', 'Mensal'),
    )
    plano = models.CharField('Plano', max_length=20, choices=PLANOS_OPCOES)

    class Meta:
        verbose_name = 'Cliente PF'
        verbose_name_plural = 'Clientes PF'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome

class ClientePJ(PessoaJuridica):
    PLANOS_OPCOES = (
        ('diaria', 'Diária'),
        ('horario_avulso', 'Horário Avulso'),
        ('mensal', 'Mensal'),
    )
    plano = models.CharField('Plano', max_length=20, choices=PLANOS_OPCOES)


    class Meta:
        verbose_name = 'Cliente PJ'
        verbose_name_plural = 'Clientes PJ'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome







