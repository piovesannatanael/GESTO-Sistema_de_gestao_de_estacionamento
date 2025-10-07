from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('estada', 'valor_calculado', 'metodo', 'data_pagamento', 'status',)
    list_filter = ('status', 'metodo',)
    search_fields = ('estada__veiculo__placa', 'estada__cliente__nome',)
