# valores/services.py
from .models import TabelaDePrecos, Desconto
from decimal import Decimal

def calcular_preco_final(estadia, nome_regra_desconto=None):
    """
    Calcula o preço final de uma estadia, aplicando descontos se aplicável.
    """
    # 1. Obter o veículo e a duração da estadia (exemplo de lógica)
    veiculo = estadia.veiculo
    horas_estadia = estadia.calcular_duracao_em_horas() # Supondo que você tenha esse método no modelo Estadia

    # 2. Encontrar o preço base na TabelaDePrecos
    try:
        preco_base_obj = TabelaDePrecos.objects.get(qtd_rodas=veiculo.qtd_rodas) # Simplificado, pode adicionar lógica de plano
        valor_base_total = preco_base_obj.valor * horas_estadia
    except TabelaDePrecos.DoesNotExist:
        # Se não encontrar um preço, retorna 0 ou lança um erro
        return 0.00

    # 3. Aplicar o desconto, se uma regra for fornecida
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
            # Se a regra de desconto não for encontrada, não faz nada e segue com o valor base
            pass

    # Garante que o valor não seja negativo
    return max(0.00, valor_final)