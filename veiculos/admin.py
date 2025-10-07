from django.contrib import admin
from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'cor', 'get_qtd_rodas_display', 'get_plano_display',)
    list_filter = ('plano', 'qtd_rodas', 'marca',)
    search_fields = ('placa', 'marca', 'modelo',)
