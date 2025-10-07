from django.contrib import admin

from .models import Modalidade


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('veiculo','ultimo_pagamento','valido_ate','plano','esta_atrasado',)
    search_fields = ('veiculo__placa',)
    list_filter = ('veiculo__plano',)

    def esta_atrasado(self, obj):
        return obj.esta_atrasado

    esta_atrasado.boolean = True
