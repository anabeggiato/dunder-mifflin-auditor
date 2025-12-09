import pandas as pd
import os

CSV_PATH = os.path.join("data", "transacoes_bancarias.csv")

def carregar_dados():
    if not os.path.exists(CSV_PATH): return None
    return pd.read_csv(CSV_PATH)

def listar_maiores_gastos(top_n: float = 5):
    """Lista as N maiores despesas da empresa."""
    df = carregar_dados()
    n_inteiro = int(top_n)
    top = df.nlargest(n_inteiro, 'valor')
    resultado = f"Top {n_inteiro} maiores gastos:\n"
    for _, row in top.iterrows():
        resultado += f"- ${row['valor']:.2f} | {row['funcionario']} ({row['categoria']})\n"
    return resultado

def analisar_gastos_por_categoria(categoria: str, valor_limite: float = None):
    """Verifica infrações de limite em uma categoria."""
    df = carregar_dados()
    df_filtrado = df[df['categoria'].str.contains(categoria, case=False, na=False)]
    
    if df_filtrado.empty: return f"Nada encontrado em '{categoria}'."
    
    if valor_limite:
        infracoes = df_filtrado[df_filtrado['valor'] > valor_limite]
        if infracoes.empty: return f"✅ Tudo certo em '{categoria}' (Lim: ${valor_limite})."
        
        res = f"ALERTA: {len(infracoes)} transações acima de ${valor_limite} em '{categoria}':\n"
        for _, row in infracoes.iterrows():
            res += f"- ${row['valor']} ({row['funcionario']})\n"
        return res
    
    # Se não passou limite, apenas lista (fallback)
    return df_filtrado.to_string()


def calcular_estatisticas_categoria(categoria: str, metrica: str = "total"):
    """
    Calcula estatísticas financeiras para uma categoria específica.
    
    Args:
        categoria: Nome da categoria (ex: 'Correio', 'Viagem').
        metrica: O que calcular? Opções: 'total' (soma), 'media', 'minimo' (menor gasto), 'maximo' (maior gasto), 'contagem' (qtd transações).
    """
    df = carregar_dados()
    # Filtro insensível a maiúsculas/minúsculas
    df_filtrado = df[df['categoria'].str.contains(categoria, case=False, na=False)]
    
    if df_filtrado.empty:
        return f"Não encontrei nenhuma transação na categoria '{categoria}'."

    valor_final = 0.0
    desc = ""

    if metrica == "total":
        valor_final = df_filtrado['valor'].sum()
        desc = "Gasto Total"
    elif metrica == "media":
        valor_final = df_filtrado['valor'].mean()
        desc = "Média de Gastos"
    elif metrica == "minimo":
        min_row = df_filtrado.loc[df_filtrado['valor'].idxmin()]
        return f"O menor gasto em '{categoria}' foi de ${min_row['valor']:.2f} por {min_row['funcionario']}."
    elif metrica == "maximo":
        max_row = df_filtrado.loc[df_filtrado['valor'].idxmax()]
        return f"O maior gasto em '{categoria}' foi de ${max_row['valor']:.2f} por {max_row['funcionario']}."
    elif metrica == "contagem":
        qtd = len(df_filtrado)
        return f"Existem {qtd} transações registradas em '{categoria}'."
    else:
        return f"Métrica '{metrica}' não reconhecida."

    return f"{desc} em '{categoria}': ${valor_final:.2f}"