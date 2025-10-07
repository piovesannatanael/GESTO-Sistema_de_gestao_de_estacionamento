from django.contrib import admin

from pagamentos_modal.models import PagamentoModal


@admin.register(PagamentoModal)
class PagamentoModalAdmin(admin.ModelAdmin):
    list_display = ('estadia', 'plano_contratado', 'valor_final', 'metodo', 'data_pagamento')
    list_filter = ('plano_contratado', 'metodo', 'data_pagamento')
    search_fields = ('estadia__veiculo__placa',)
    readonly_fields = ('valor_bruto', 'desconto_aplicado', 'valor_final')
