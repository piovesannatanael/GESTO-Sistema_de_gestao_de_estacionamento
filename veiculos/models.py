from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField
from clientes.models import ClienteGeral
from valores.models import Plano, Categoria


class Veiculo(models.Model):

    placa = models.CharField('Placa', max_length=8, unique=True)
    marca = models.CharField('Marca', max_length=50)
    modelo = models.CharField('Modelo', max_length=50)
    cor = models.CharField('Cor', max_length=30)
    categoria_cnh = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True,verbose_name='Categoria do Veículo',
        limit_choices_to={'status': True})
    plano = models.ForeignKey(Plano,on_delete=models.SET_NULL, null=True,blank=True, verbose_name='Plano')
    clientes = models.ManyToManyField(ClienteGeral,verbose_name='Proprietário(s)',related_name='veiculos')
    foto = StdImageField('Foto', upload_to='carros', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = [Upper('placa')]

    def __str__(self):
        return f'{self.placa} ({self.modelo})'
