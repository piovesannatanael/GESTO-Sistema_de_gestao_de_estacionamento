from django.contrib import admin
from django.utils.html import format_html
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    fields = ('estadia', 'valor_total', 'forma', 'status', 'data_pagamento', 'observacao')
    list_display = ('id', 'estadia_display', 'valor_total', 'forma_display', 'status_display',
                    'data_pagamento_formatado')
    readonly_fields = ['data_pagamento_formatado']
    search_fields = ('estadia__veiculo__placa', 'estadia__cliente__nome', 'forma')
    list_filter = ('status', 'forma', 'data_pagamento')

    def estadia_display(self, obj):
        if obj.estadia:
            return f"{obj.estadia.veiculo.placa} - {obj.estadia.cliente.nome}"
        return "-"

    estadia_display.short_description = 'Estadia'

    def forma_display(self, obj):
        return obj.get_forma_display()

    forma_display.short_description = 'Forma de Pagamento'

    def status_display(self, obj):
        status_colors = {
            'PENDENTE': 'orange',
            'PAGO': 'green',
            'CANCELADO': 'red'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_display.short_description = 'Status'

    def data_pagamento_formatado(self, obj):
        if obj.data_pagamento:
            return obj.data_pagamento.strftime("%d/%m/%Y %H:%M")
        return "Não pago"

    data_pagamento_formatado.short_description = 'Data do Pagamento'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('estadia', 'estadia__veiculo', 'estadia__cliente')