from django.core.exceptions import ValidationError
from django.db import models


class Plano(models.Model):
    PLANOS_CHOICES = (
        ('Avulso', 'Horário Avulso'),
        ('Diaria', 'Diária'),
        ('Semanal', 'Semanal'),
        ('Mensal', 'Mensal'),
        ('Outro', 'Outro plano'),
    )

    nome = models.CharField('Nome do Plano',choices=PLANOS_CHOICES,  max_length=50, unique=True, default='Avulso')
    valor = models.DecimalField('Valor Base (R$)', max_digits=8, decimal_places=2)
    status = models.BooleanField('Ativo', default=True, help_text='Marque para ativar o plano')
    descricao = models.TextField('Descrição', max_length=300, blank=True, null=True)


    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"


class Desconto(models.Model):
    DESCONTO_CHOICES = (
        ('PERCENTUAL', 'Percentual (%)'),
        ('FIXO', 'Valor Fixo (R$)'),
    )

    nome = models.CharField('Nome do desconto', max_length=100, help_text='Ex: Desconto para funcionário')
    tipo = models.CharField('Tipo de desconto', max_length=20, choices=DESCONTO_CHOICES, default='PERCENTUAL')
    valor = models.DecimalField('Valor do desconto', max_digits=8, decimal_places=2,
                                help_text='Desconto máximo de 100% ou de R$100')
    descricao = models.TextField('Descrição', max_length=300, blank=True, null=True)
    status = models.BooleanField('Ativo', default=True, help_text='Marque para ativar este desconto')

    class Meta:
        verbose_name = 'Desconto'
        verbose_name_plural = 'Descontos'

    def clean(self):
        super().clean()

        if self.tipo == 'PERCENTUAL' and self.valor > 100:
            raise ValidationError({
                'valor': 'O desconto em formato percentual não pode ser maior que 100.'
            })
        elif self.tipo == 'FIXO' and self.valor > 100:
            raise ValidationError({
                'valor': 'O desconto em maximo não pode ser maior que 100 reais'
            })

    def __str__(self):
        if self.tipo == 'PERCENTUAL':
            return f"{self.nome} ({self.valor}%)"
        return f"{self.nome} (R$ {self.valor})"



class Extra(models.Model):
    EXTRA_CHOICES = (
        ('PERCENTUAL', 'Percentual (%)'),
        ('FIXO', 'Valor Fixo (R$)'),
    )

    nome = models.CharField('Nome do adicional', max_length=100, help_text='Ex: ')
    tipo = models.CharField('Tipo do adicional', max_length=20, choices=EXTRA_CHOICES, default='PERCENTUAL')
    valor = models.DecimalField('Valor a adicionar (R$)', max_digits=8, decimal_places=2, help_text='Somente números')
    descricao = models.TextField('Descrição', max_length=300, blank=True, null=True)
    status = models.BooleanField('Ativo', default=True, help_text='Marque para ativar este valor extra')


    class Meta:
        verbose_name = 'Valor Extra'
        verbose_name_plural = 'Valores Extras'

    def __str__(self):
        if self.tipo == 'PERCENTUAL':
            return f"{self.nome} (+{self.valor}%)"
        return f"{self.nome} (+ R$ {self.valor})"




class Categoria(models.Model):

    CNH_CHOICES = (
        ('A', 'A - Motocicleta'),
        ('B', 'B - Carro'),
        ('C', 'C - Caminhão'),
        ('D', 'D - Ônibus/Van'),
        ('E', 'E - Veículos com reboque'),
        ('O', 'Outro tipo de categoria'),
    )
    cnh = models.CharField('Categoria de CNH', max_length=5, choices=CNH_CHOICES, unique=True, default="A")
    valor_hora = models.DecimalField('Valor adicional pela categoria (%)', max_digits=8, decimal_places=2)
    status = models.BooleanField('Ativo', default=True, help_text='Marque para ativar a categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return f'{self.cnh} (+{self.valor_hora} %)'