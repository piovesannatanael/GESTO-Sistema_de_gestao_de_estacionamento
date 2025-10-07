from django.db import models
from django.utils import timezone
from veiculos.models import Veiculo
from clientes.models import ClienteGeral
from funcionarios.models import Funcionario
from vagas.models import Vaga


class Estadia(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    cliente = models.ForeignKey(ClienteGeral, on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True, blank=True)
    plano = models.CharField('Plano', max_length=20, choices=Veiculo.PLANOS_CHOICES, null=True, blank=True)
    data_chegada = models.DateTimeField(default=timezone.now)
    data_saida = models.DateTimeField(null=True, blank=True)
    finalizada = models.BooleanField(default=False)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        permissions = (('encerrar_estadia','Permite fazer o encerramento de uma estadia'),)
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['-data_chegada']

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'

    def save(self, *args, **kwargs):
        vaga_original = None
        if self.pk:
            try:
                vaga_original = Estadia.objects.get(pk=self.pk).vaga
            except Estadia.DoesNotExist:
                pass
        super().save(*args, **kwargs)

        if self.vaga:
            if self.finalizada:
                self.vaga.status = 'livre'
            else:
                self.vaga.status = 'ocupada'
            self.vaga.save()

        if vaga_original and vaga_original != self.vaga:
            vaga_original.status = 'livre'
            vaga_original.save()


#
# from django.db import models
# from django.utils import timezone
# from decimal import Decimal
# from datetime import timedelta
#
# # Importe os models que você precisa referenciar
# from veiculos.models import Veiculo
# from clientes.models import ClienteGeral
# from funcionarios.models import Funcionario
# from vagas.models import Vaga
#
# # ==============================================================================
# # PREÇO BASE POR HORA CONFIRMADO
# # ==============================================================================
# PRECO_HORA_BASE = Decimal('10.00')
# # ==============================================================================
#
#
# class Estadia(models.Model):
#     veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, verbose_name='Veículo')
#     cliente = models.ForeignKey(ClienteGeral, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
#     funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Funcionário')
#     vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Vaga')
#     plano = models.CharField('Plano', max_length=20, choices=Veiculo.PLANOS_CHOICES, null=True, blank=True)
#     data_chegada = models.DateTimeField('Data de Chegada', default=timezone.now)
#     data_saida = models.DateTimeField('Data de Saída', null=True, blank=True)
#     finalizada = models.BooleanField('Finalizada', default=False)
#     valor_total = models.DecimalField('Valor Total', max_digits=8, decimal_places=2, null=True, blank=True)
#
#     class Meta:
#         permissions = (('encerrar_estadia', 'Permite fazer o encerramento de uma estadia'),)
#         verbose_name = 'Estadia'
#         verbose_name_plural = 'Estadias'
#         ordering = ['-data_chegada']
#
#     def __str__(self):
#         return f'{self.veiculo.placa} - {self.data_chegada.strftime("%d/%m/%Y %H:%M")}'
#
#     def calcular_valor_final(self, metodo_pagamento='CARTAO_DEBITO'):
#         """
#         Calcula o valor final da estada aplicando todas as regras de negócio para pagamentos_avulso avulsos.
#         """
#         if self.plano != 'Avulso' or not self.data_saida:
#             return Decimal('0.00')
#
#         # --- 1. Calcular Duração e Preço Base ---
#         duracao = self.data_saida - self.data_chegada
#         horas_totais = (duracao.total_seconds() + 3599) // 3600
#         if horas_totais < 1:
#             horas_totais = 1  # Mínimo de 1 hora de cobrança
#
#         preco_base = Decimal(horas_totais) * PRECO_HORA_BASE
#
#         # --- 2. Aplicar Acréscimo por Categoria do Veículo ---
#         qtd_rodas = self.veiculo.qtd_rodas
#         percentual_acrescimo = Decimal('0.00')
#         if qtd_rodas == 2:
#             percentual_acrescimo = Decimal('0.02')  # 2%
#         elif qtd_rodas >= 3:
#             percentual_acrescimo = Decimal('0.03')  # 3% para 3 ou mais rodas
#
#         valor_com_acrescimo = preco_base * (Decimal('1.0') + percentual_acrescimo)
#         valor_a_cobrar = valor_com_acrescimo
#
#         # --- 3. Aplicar Multa por Longa Permanência (> 12h) ---
#         if duracao > timedelta(hours=12):
#             multa = valor_a_cobrar * Decimal('0.50')  # 50%
#             valor_a_cobrar += multa
#
#         # --- 4. Aplicar Descontos (o melhor desconto prevalece) ---
#         desconto_funcionario = Decimal('0.00')
#         desconto_pagamento = Decimal('0.00')
#
#         if self.cliente and self.cliente.cpf:
#             is_funcionario = Funcionario.objects.filter(cpf=self.cliente.cpf).exists()
#             if is_funcionario:
#                 desconto_funcionario = valor_a_cobrar * Decimal('0.20')  # 20%
#
#         if metodo_pagamento in ['PIX', 'DINHEIRO']:
#             desconto_pagamento = valor_a_cobrar * Decimal('0.15')  # 15%
#
#         maior_desconto = max(desconto_funcionario, desconto_pagamento)
#         valor_a_cobrar -= maior_desconto
#
#         return round(valor_a_cobrar, 2)
#
#     def save(self, *args, **kwargs):
#         vaga_original = None
#         if self.pk:
#             try:
#                 vaga_original = Estadia.objects.get(pk=self.pk).vaga
#             except Estadia.DoesNotExist:
#                 pass
#
#         # Lógica de cálculo do valor_total adicionada aqui
#         if self.finalizada and self.data_saida and not self.valor_total:
#             self.valor_total = self.calcular_valor_final()
#
#         super().save(*args, **kwargs)
#
#         # Sua lógica original de gerenciamento de vagas foi mantida
#         if self.vaga:
#             if self.finalizada:
#                 self.vaga.status = 'livre'
#             else:
#                 self.vaga.status = 'ocupada'
#             self.vaga.save()
#
#         if vaga_original and vaga_original != self.vaga:
#             vaga_original.status = 'livre'
#             vaga_original.save()
