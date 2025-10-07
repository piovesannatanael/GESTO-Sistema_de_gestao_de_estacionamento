
from django.contrib import admin
from django.utils.html import format_html

from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    fields = ('nome', 'cpf', 'data_nascimento', 'funcao', 'data_admissao', 'fone', 'email', 'endereco', 'foto')
    list_display = ('nome', 'fone','email','funcao')
    readonly_fields = ['fotografia']
    search_fields = ('nome', 'fone')
    list_filter = ('funcao',)


    def fotografia(self, obj):
        if obj.foto:
            return format_html('<img width="75px" src="{}" />', obj.foto.url)
        pass