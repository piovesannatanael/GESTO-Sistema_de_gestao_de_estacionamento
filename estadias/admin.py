from django.contrib import admin

from estadias.models import Estadia


@admin.register(Estadia)
class EstadiaAdmin(admin.ModelAdmin):
    list_display = ('veiculo','cliente','vaga','data_chegada','data_saida','finalizada','plano',)
    list_filter = ('finalizada', 'plano', 'vaga',)
    search_fields = ('veiculo__placa', 'cliente__nome', 'vaga__codigo')
