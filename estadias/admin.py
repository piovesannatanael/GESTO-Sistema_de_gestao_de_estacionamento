from django.contrib import admin

from estadias.models import Estadia


@admin.register(Estadia)
class EstadiaAdmin(admin.ModelAdmin):
    list_display = ('veiculo','cliente','vaga','data_chegada','data_saida','finalizada','plano_veiculo',)
    list_filter = ('finalizada', 'veiculo__plano', 'vaga',)
    search_fields = ('veiculo__placa', 'cliente__nome', 'vaga__codigo')

    @admin.display(description='Plano do Veículo')
    def plano_veiculo(self, obj):
        if obj.veiculo and obj.veiculo.plano:
            return obj.veiculo.plano.nome
        return "N/A"