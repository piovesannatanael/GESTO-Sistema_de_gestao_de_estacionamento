# valores/services.py
from .models import TabelaDePrecos, Desconto
from decimal import Decimal

def calcular_preco_final(estadia, nome_regra_desconto=None):

    veiculo = estadia.veiculo
    horas_estadia = estadia.calcular_duracao_em_horas() # Supondo que você tenha esse método no modelo Estadia

    try:
        preco_base_obj = TabelaDePrecos.objects.get(qtd_rodas=veiculo.qtd_rodas) # Simplificado, pode adicionar lógica de plano
        valor_base_total = preco_base_obj.valor * horas_estadia
    except TabelaDePrecos.DoesNotExist:
        return 0.00

    valor_final = valor_base_total
    if nome_regra_desconto:
        try:
            regra = Desconto.objects.get(nome__iexact=nome_regra_desconto, ativo=True)
            if regra.tipo == 'PERCENTUAL':
                desconto = valor_base_total * (regra.valor / 100)
                valor_final = valor_base_total - desconto
            elif regra.tipo == 'FIXO':
                valor_final = valor_base_total - regra.valor
        except Desconto.DoesNotExist:
            pass

    return max(0.00, valor_final)