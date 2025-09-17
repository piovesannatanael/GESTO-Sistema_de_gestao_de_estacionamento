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
        abstract = True

    def __str__(self):
        return self.nome

class PessoaFisica(Pessoa):
    cpf = models.DecimalField('CPF', max_digits=11, unique=True, help_text='Digite o CPF')
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True, help_text='Data de nascimento')

    class Meta:
        abstract = True

    def __str__(self):
        return self.cpf

class PessoaJuridica(Pessoa):
    empresa = models.CharField('Empresa', max_length=100, help_text='Nome da empresa')
    cnpj = models.DecimalField('CNPJ', max_digits=14, unique=True, help_text='Digite o CNPJ da empresa')

    class Meta:
        abstract = True

    def __str__(self):
        return self.empresa

class ClientePF(PessoaFisica):
    num_cadastro = models.DecimalField('N° cadastro', max_digits=5, help_text='Numero de cadastro')
    plano = models.CharField('Plano', max_length=15, help_text='Tipo do plano')

    class Meta:
        verbose_name = 'Cliente PF'
        verbose_name_plural = 'Clientes PF'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome

class ClientePJ(PessoaJuridica):
    num_cadastro = models.DecimalField('N° cadastro', max_digits=5, help_text='Numero de cadastro da empresa')
    plano = models.CharField('Plano', max_length=15, help_text='Tipo do plano da empresa')

    class Meta:
        verbose_name = 'Cliente PJ'
        verbose_name_plural = 'Clientes PJ'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome