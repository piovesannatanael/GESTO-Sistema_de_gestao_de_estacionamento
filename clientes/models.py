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
    cpf = models.DecimalField('CPF', max_digits=11, unique=True, decimal_places=0, help_text='Digite o CPF')
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


class Cliente(models.Model):
    TIPO_PESSOA_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    # --- Campos Comuns ---
    nome = models.CharField('Nome', max_length=100, help_text='Nome ou Razão Social')
    fone = models.CharField('Fone', max_length=15, help_text='Número de telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='E-mail', unique=True)
    endereco = models.CharField('Endereço', max_length=300, help_text='Endereço completo')
    foto = StdImageField('Foto', upload_to='clientes', delete_orphans=True, null=True, blank=True)

    # --- Campo de Controle ---
    tipo_pessoa = models.CharField('Tipo de Pessoa', max_length=2, choices=TIPO_PESSOA_CHOICES, default='PF')

    # --- Campos de Pessoa Física ---
    cpf = models.CharField('CPF', max_length=14, unique=True, null=True, blank=True, help_text='Digite o CPF')
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True, help_text='Data de nascimento')

    # --- Campos de Pessoa Jurídica ---
    cnpj = models.CharField('CNPJ', max_length=18, unique=True, null=True, blank=True,
                            help_text='Digite o CNPJ da empresa')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = [Upper('nome')]

    def __str__(self):
        return self.nome

'''class Cliente(PessoaFisica or PessoaJuridica):

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome

'''
'''class ClientePF(PessoaFisica):
    num_cadastro = models.DecimalField('N° cadastro', max_digits=5, decimal_places=0 ,help_text='Numero de cadastro')
    plano = models.CharField('Plano', max_length=15, help_text='Tipo do plano')

    class Meta:
        verbose_name = 'Cliente PF'
        verbose_name_plural = 'Clientes PF'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome

class ClientePJ(PessoaJuridica):
    num_cadastro = models.DecimalField('N° cadastro', max_digits=5, decimal_places=0, help_text='Numero de cadastro da empresa')
    plano = models.CharField('Plano', max_length=15, help_text='Tipo do plano da empresa')

    class Meta:
        verbose_name = 'Cliente PJ'
        verbose_name_plural = 'Clientes PJ'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome

"""class Cliente(ClientePJ or ClientePF):

tornar as classes clientes pf e pj como abstratas e unificar como cliente
"""
'''