from django.db import models
from django.db.models.functions import Upper
from clientes.models import ClienteGeral
from valores.models import Plano, Categoria


class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=10, unique=True)
    marca = models.CharField('Marca', max_length=50, null=True, blank=True)
    modelo = models.CharField('Modelo', max_length=50, null=True, blank=True)
    cor = models.CharField('Cor', max_length=30, null=True, blank=True)
    foto = models.ImageField('Foto', upload_to='static/veiculos', null=True, blank=True)
    clientes = models.ManyToManyField(ClienteGeral,related_name='veiculos',verbose_name='Clientes',blank=False)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Plano')
    categoria_cnh = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, verbose_name='Categoria do Veículo',limit_choices_to={'status': True})
    data_vencimento_plano = models.DateField('Data de Vencimento do Plano',null=True,blank=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = [Upper('placa')]

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    def calcular_data_vencimento(self, data_base=None):
        from django.utils import timezone

        if self.plano.is_avulso():
            return None

        if not data_base:
            data_base = timezone.now().date()

        return self.plano.calcular_validade(data_base)

    def atualizar_vencimento_plano(self, data_pagamento=None):
        if self.plano.is_avulso():
            self.data_vencimento_plano = None
        else:
            self.data_vencimento_plano = self.calcular_data_vencimento(data_pagamento)
        self.save()

    @property
    def plano_esta_valido(self):
        if self.plano.is_avulso():
            return True

        if not self.data_vencimento_plano:
            return False

        from django.utils import timezone
        return timezone.now().date() <= self.data_vencimento_plano