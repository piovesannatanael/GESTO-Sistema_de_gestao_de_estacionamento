
from django.contrib import admin
from django.utils.html import format_html

from .models import ClienteGeral

@admin.register(ClienteGeral)
class ClienteGeralAdmin(admin.ModelAdmin):
    fields = ('tipo_cliente', 'nome', 'fone', 'email', 'endereco', 'foto','cpf', 'data_nascimento', 'empresa', 'cnpj','fotografia')
    list_display = ('nome', 'fone','email')
    readonly_fields = ['fotografia']
    search_fields = ('nome', 'fone')


    def fotografia(self, obj):
        if obj.foto:
            return format_html('<img width="75px" src="{}" />', obj.foto.url)
        pass