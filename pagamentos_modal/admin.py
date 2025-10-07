from django.contrib import admin

from pagamentos_modal.models import PagamentoModalidade


@admin.register(PagamentoModalidade)
class PagamentoModalidadeAdmin(admin.ModelAdmin):
    list_display = ('modalidade', 'valor_pago', 'data_pagamento', 'metodo',)
    list_filter = ('metodo',)
    search_fields = ('modalidade__veiculo__placa',)
