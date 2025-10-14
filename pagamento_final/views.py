# def enviar_email_recibo_avulso(self, pagamento):
#     try:
#         estadia = pagamento.estadia
#         cliente = estadia.cliente
#
#         if not cliente or not cliente.email:
#             self.logger.warning(f"Pagamento (ID: {pagamento.pk}) sem cliente ou e-mail associado.")
#             return False
#
#         dados = {
#             'cliente_nome': cliente.nome,
#             'veiculo_placa': estadia.veiculo.placa,
#             'veiculo_modelo': estadia.veiculo.modelo,
#             'data_chegada': estadia.data_chegada,
#             'data_saida': estadia.data_saida,
#             'valor_bruto': pagamento.valor_bruto,
#             'desconto_aplicado': pagamento.desconto_aplicado,
#             'valor_final': pagamento.valor_final,
#             'metodo_pagamento': pagamento.get_metodo_display(),
#             'data_pagamento': pagamento.data_pagamento,
#         }
#
#         texto_email = render_to_string('emails/recibo_pgto_avulso.txt', dados)
#         html_email = render_to_string('emails/recibo_pgto_avulso.html', dados)
#         recipient = [cliente.email]
#
#         send_mail(
#             subject='GESTO - Recibo de Pagamento',
#             message=texto_email,
#             from_email='piovesannatanael@gmail.com',
#             recipient_list=recipient,
#             html_message=html_email,
#             fail_silently=False
#         )
#         self.logger.info(f"E-mail de recibo enviado para {recipient} (Pagamento ID: {pagamento.pk})")
#         return True
#     except Exception as e:
#         self.logger.exception(f"Falha ao enviar e-mail de recibo para o pagamento {pagamento.pk}: {e}")
#         return False