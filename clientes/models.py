from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    fone = models.CharField('Fone', max_length=12, help_text='Número de telefone (Apenas números)', unique=True)
    email = models.EmailField('E-mail', max_length=100, help_text='E-mail', unique=True)
    endereco = models.CharField('Endereço', max_length=300, help_text='Endereço completo')
    foto = StdImageField('Foto', upload_to='static/pessoas', delete_orphans=True, null=True, blank=True)

    class Meta:
        abstract = True
        # verbose_name = 'Pessoa'
        # verbose_name_plural = 'Pessoas'
        # ordering = [Upper('nome')]'

    def __str__(self):
        return self.nome


class PessoaFisica(Pessoa):
    cpf = models.CharField('CPF', max_length=14, unique=True, null=True, blank=True, help_text='Digite o CPF')
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True, help_text='Data de nascimento')

    class Meta:
        abstract = True

    def __str__(self):
        return self.cpf


class PessoaJuridica(Pessoa):
    empresa = models.CharField('Empresa', max_length=100, help_text='Nome da empresa')
    cnpj = models.DecimalField('CNPJ', max_digits=14, unique=True, decimal_places=0,
                               help_text='Digite o CNPJ da empresa')

    class Meta:
        abstract = True

    def __str__(self):
        return self.empresa


class ClienteGeral(Pessoa):
    TIPO_CLIENTE_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )
    tipo_cliente = models.CharField('Tipo de Cliente', max_length=2, choices=TIPO_CLIENTE_CHOICES)
    cpf = models.CharField('CPF ', max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    empresa = models.CharField('Nome da Empresa', max_length=100, null=True, blank=True)
    cnpj = models.CharField('CNPJ (Apenas números)', max_length=18, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = [Upper('nome'), Upper('empresa')]

    def __str__(self):
        if self.tipo_cliente == 'PJ' and self.empresa:
            return f'{self.empresa} ({self.nome})'
        return self.nome

    def clean(self):
        super().clean()
        if self.tipo_cliente == 'PF':
            if not self.cpf:
                raise ValidationError('CPF é obrigatório para Pessoa Física.')
            self.cnpj = None
            self.empresa = None
        elif self.tipo_cliente == 'PJ':
            if not self.cnpj:
                raise ValidationError('CNPJ é obrigatório para Pessoa Jurídica.')
            if not self.empresa:
                raise ValidationError('Nome da Empresa é obrigatório para Pessoa Jurídica.')
            self.cpf = None
            self.data_nascimento = None
