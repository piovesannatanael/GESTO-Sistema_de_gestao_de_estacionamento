# vagas/models.py

from django.db import models
from django.db.models.functions import Upper


class Vaga(models.Model):
    STATUS = (
        ('livre', 'Livre'),
        ('ocupada', 'Ocupada'),
        ('manutencao', 'Em Manutenção'),
    )

    codigo = models.CharField('Código da Vaga', max_length=10, unique=True, help_text='Ex: A01, B12, etc.')
    status = models.CharField('Status', max_length=10, choices=STATUS, default='L')

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'
        ordering = [Upper('codigo')]

    def __str__(self):
        return self.codigo