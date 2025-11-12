from django.contrib import admin
from .models import Vaga


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'status')
    list_filter = ('status',)
    search_fields = ('codigo',)
