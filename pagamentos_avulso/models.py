# from django.db import models
# from django.utils import timezone
# from estadias.models import Estadia
# from funcionarios.models import Funcionario
# from decimal import Decimal
# from datetime import timedelta
#
# PRECO_HORA_BASE = Decimal('15.00')
#
# class PagamentoAvulso(models.Model):
#     METODO_CHOICES = (
#         ('PIX', 'PIX'),
#         ('DINHEIRO', 'Dinheiro'),
#         ('CARTAO', 'Cartão'),
#     )
#
#     STATUS_CHOICES = (
#         ('PENDENTE', 'Pendente'),
#         ('PAGO', 'Pago'),
#     )
#
#     estadia = models.OneToOneField(Estadia,on_delete=models.PROTECT,related_name='pagamento_avulso')
#     metodo = models.CharField('Método', max_length=20, choices=METODO_CHOICES, default='Cartão')
#
#     valor_bruto = models.DecimalField('Valor Bruto (sem descontos)',max_digits=10,decimal_places=2,null=True, blank=True)
#     desconto_aplicado = models.DecimalField('Desconto Aplicado',
#         max_digits=10,decimal_places=2,default=0.00)
#     valor_final = models.DecimalField('Valor Final (a pagar)',max_digits=10,decimal_places=2,null=True, blank=True)
#
#     data_pagamento = models.DateTimeField(default=timezone.now)
#     status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
#
#     class Meta:
#         verbose_name = 'Pagamento Avulso'
#         verbose_name_plural = 'Pagamentos Avulsos'
#
#     def __str__(self):
#         placa = getattr(self.estadia.veiculo, 'placa', '??') if self.estadia else '??'
#         return f'Pagamento para a estada do veículo {placa}'
#
#     def calcular_valores(self):
#         if not self.estadia or not self.estadia.data_saida:
#             return {'valor_bruto': Decimal('0.00'), 'desconto': Decimal('0.00'), 'valor_final': Decimal('0.00')}
#
#         duracao = self.estadia.data_saida - self.estadia.data_chegada
#         horas_arredondadas = int((duracao.total_seconds() + 3599) // 3600)
#         preco_base = PRECO_HORA_BASE * max(1, horas_arredondadas)
#
#         veiculo = self.estadia.veiculo
#         acrescimo = Decimal('0.00')
#         qtd_rodas = getattr(veiculo, 'qtd_rodas', None)
#         try:
#             qtd_rodas_int = int(qtd_rodas)
#         except Exception:
#             qtd_rodas_int = None
#
#         if qtd_rodas_int == 2:
#             acrescimo = preco_base * 0.02
#         elif qtd_rodas_int and qtd_rodas_int >= 3:
#             acrescimo = preco_base * 0.03
#
#         valor_com_acrescimo = preco_base + acrescimo
#
#         valor_bruto = valor_com_acrescimo
#         if duracao > timedelta(hours=12):
#             multa = valor_bruto * Decimal('0.50')
#             valor_bruto += multa
#
#         desconto_funcionario = Decimal('0.00')
#         desconto_pagamento = Decimal('0.00')
#
#         if self.estadia.cliente and hasattr(self.estadia.cliente, 'cpf'):
#             is_funcionario = Funcionario.objects.filter(cpf=self.estadia.cliente.cpf).exists()
#             if is_funcionario:
#                 desconto_funcionario = valor_bruto * 0.20
#
#         if self.metodo in ['PIX', 'DINHEIRO']:
#             desconto_pagamento = valor_bruto * 0.15
#
#         maior_desconto = max(desconto_funcionario, desconto_pagamento)
#         valor_final = valor_bruto - maior_desconto
#
#         return {
#             'valor_bruto': round(valor_bruto, 2),
#             'desconto': round(maior_desconto, 2),
#             'valor_final': round(valor_final, 2),
#         }
#
#     def calcular_valor(self):
#         return self.calcular_valores()
#
#     @property
#     def valor_calculado(self):
#         if self.valor_final is not None:
#             return self.valor_final
#         vals = self.calcular_valores()
#         return vals.get('valor_final', 0.00)
#
#     def save(self, *args, **kwargs):
#         valores = self.calcular_valores()
#         self.valor_bruto = valores['valor_bruto']
#         self.desconto_aplicado = valores['desconto']
#         self.valor_final = valores['valor_final']
#
#         if self.status == 'PAGO':
#             self.estadia.valor_total = self.valor_final
#             self.estadia.finalizada = True
#             self.estadia.save()
#
#         super().save(*args, **kwargs)
