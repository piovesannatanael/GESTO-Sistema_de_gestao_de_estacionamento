from django.contrib import admin
from .models import PagamentoAvulso


@admin.register(PagamentoAvulso)
class PagamentoAvulsoAdmin(admin.ModelAdmin):
    list_display = ('estadia', 'valor_final', 'metodo', 'data_pagamento')
    list_filter = ('metodo', 'data_pagamento')
    search_fields = ('estadia__veiculo__placa',)
    readonly_fields = ('valor_bruto', 'desconto_aplicado', 'valor_final')
