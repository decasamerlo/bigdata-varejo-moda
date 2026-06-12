# -*- coding: utf-8 -*-
"""
=============================================================
  ANÁLISE DE VENDAS - VAREJO DE MODA
  Projeto de Extensão - Faculdade Estácio de Sá
=============================================================

  Este script realiza a leitura e análise inicial dos dados
  de vendas de uma loja de roupas, gerando informações
  úteis para tomada de decisão.

  Bibliotecas utilizadas:
    - pandas: manipulação e análise de dados
    - os: verificação de caminhos de arquivos
=============================================================
"""

# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================
# pandas é a biblioteca principal para análise de dados em Python
# ela trabalha com "DataFrames" (tabelas como no Excel)
import pandas as pd

# os serve para verificar se os arquivos existem antes de ler
import os

# ============================================================
# 2. CAMINHO DOS ARQUIVOS
# ============================================================
# Definimos a pasta onde estão os arquivos CSV
# Isso evita digitar o caminho completo toda vez
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "")

# Dicionário com os nomes dos arquivos e seus separadores
# Alguns CSVs usam vírgula (,) e outros usam ponto e vírgula (;)
ARQUIVOS = {
    "Vendas_Mes_Ano": {
        "arquivo": "Total-Vendas-Mes-Ano.csv",
        "separador": ","
    },
    "Vendas_Produto": {
        "arquivo": "Total-Vendas-Produto.csv",
        "separador": ","
    },
    "Vendas_Cliente": {
        "arquivo": "Vendas-Cliente-2024-2025.csv",
        "separador": ";"
    },
    "Vendas_Produto_Detalhado": {
        "arquivo": "Vendas-Produto-2024-2025.csv",
        "separador": ","
    }
}

# ============================================================
# 3. FUNÇÃO PARA LER ARQUIVOS CSV
# ============================================================
def ler_csv(nome, config):
    """
    Lê um arquivo CSV e retorna um DataFrame.

    Parâmetros:
        nome (str): Nome amigável do dataset
        config (dict): Dicionário com 'arquivo' e 'separador'

    Retorna:
        pd.DataFrame ou None se houver erro
    """
    caminho = os.path.join(PASTA_DADOS, config["arquivo"])

    # Verifica se o arquivo existe antes de tentar ler
    if not os.path.exists(caminho):
        print(f"  [ERRO] Arquivo não encontrado: {config['arquivo']}")
        return None

    try:
        # encoding='latin-1' resolve problemas de acentuação
        # sep define o caractere separador das colunas
        df = pd.read_csv(
            caminho,
            sep=config["separador"],
            encoding="latin-1"
        )
        print(f"  [OK] Arquivo '{config['arquivo']}' lido com sucesso!")
        return df

    except Exception as e:
        # Se der erro, mostra qual foi o problema
        print(f"  [ERRO] Falha ao ler '{config['arquivo']}': {e}")
        return None

# ============================================================
# 4. FUNÇÃO PARA CONVERTER COLUNAS NUMÉERICAS
# ============================================================
def converter_colunas_numericas(df, colunas):
    """
    Converte colunas que estão como texto (string) para números.
    O formato brasileiro usa vírgula como separador decimal
    (ex: 1.234,56) e o Python espera ponto (ex: 1234.56).

    Parâmetros:
        df (pd.DataFrame): DataFrame original
        colunas (list): Lista com nomes das colunas a converter

    Retorna:
        pd.DataFrame com as colunas convertidas
    """
    for coluna in colunas:
        if coluna in df.columns:
            # Verifica se a coluna NÃO é numérica
            # (pandas 3.x usa "str", versões antigas usam "object")
            if not pd.api.types.is_numeric_dtype(df[coluna]):
                # Remove pontos de milhar e substitui vírgula por ponto
                # Ex: "1.234,56" → "1234.56" → 1234.56
                df[coluna] = (
                    df[coluna]
                    .astype(str)
                    .str.replace(".", "", regex=False)  # Remove pontos de milhar
                    .str.replace(",", ".", regex=False)  # Vírgula → ponto
                    .str.replace("%", "", regex=False)   # Remove percentual
                    .str.strip()                         # Remove espaços
                )
                # Converte para número; valores inválidos viram NaN
                df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df

# ============================================================
# 5. FUNÇÃO PARA EXIBIR INFORMAÇÕES GERAIS DO DATAFRAME
# ============================================================
def exibir_info(nome, df):
    """
    Exibe informações gerais sobre o DataFrame:
    - Dimensões (linhas x colunas)
    - Nomes das colunas
    - Tipos de dados
    - Primeiras e últimas linhas
    """
    print(f"\n{'='*60}")
    print(f"  DATASET: {nome}")
    print(f"{'='*60}")

    # .shape retorna (linhas, colunas)
    linhas, colunas = df.shape
    print(f"\n  Dimensões: {linhas} linhas x {colunas} colunas")

    # .columns retorna os nomes de todas as colunas
    print(f"\n  Colunas:")
    for i, coluna in enumerate(df.columns, 1):
        print(f"    {i}. {coluna}")

    # .dtypes mostra o tipo de dado de cada coluna
    # (object = texto, int64 = número inteiro, float64 = número decimal)
    print(f"\n  Tipos de dados:")
    print(df.dtypes.to_string().replace("\n", "\n    "))

    # .head() mostra as primeiras 5 linhas (padrão)
    print(f"\n  --- Primeiras 5 linhas ---")
    print(df.head().to_string(index=False))

    # .tail() mostra as últimas 5 linhas
    print(f"\n  --- Últimas 5 linhas ---")
    print(df.tail().to_string(index=False))

    # .describe() mostra estatísticas resumidas (média, mediana, etc.)
    # só funciona para colunas numéricas
    print(f"\n  --- Estatísticas resumidas ---")
    print(df.describe().to_string())

    # Verificar valores nulos (NaN) é importante para saber se faltam dados
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
        print(f"\n  Valores nulos por coluna:")
        print(nulos[nulos > 0].to_string().replace("\n", "\n    "))
    else:
        print(f"\n  [OK] Nenhum valor nulo encontrado.")

    print()

# ============================================================
# 5. FUNÇÃO PARA ORDENAR DADOS
# ============================================================
def ordenar_dados(nome, df, coluna, Crescente=True):
    """
    Ordena o DataFrame por uma coluna específica.

    Parâmetros:
        nome (str): Nome do dataset
        df (pd.DataFrame): DataFrame a ser ordenado
        coluna (str): Nome da coluna para ordenar
        Crescente (bool): True = menor para maior
    """
    # Verifica se a coluna existe no DataFrame
    if coluna not in df.columns:
        print(f"  [AVISO] Coluna '{coluna}' não existe no dataset '{nome}'")
        return None

    print(f"\n  --- Ordenação por '{coluna}' (crescente={Crescente}) ---")
    # .sort_values() ordena o DataFrame
    # ascending=True ordena do menor para o maior
    # ascending=False ordena do maior para o menor
    df_ordenado = df.sort_values(by=coluna, ascending=Crescente)
    print(df_ordenado.head(10).to_string(index=False))
    return df_ordenado

# ============================================================
# 6. FUNÇÃO PARA FILTRAR DADOS
# ============================================================
def filtrar_dados(nome, df, coluna, valor):
    """
    Filtra o DataFrame mostrando apenas linhas onde
    a coluna tem um valor específico.

    Parâmetros:
        nome (str): Nome do dataset
        df (pd.DataFrame): DataFrame original
        coluna (str): Coluna para filtrar
        valor: Valor a ser procurado
    """
    if coluna not in df.columns:
        print(f"  [AVISO] Coluna '{coluna}' não existe no dataset '{nome}'")
        return None

    print(f"\n  --- Filtro: {coluna} = {valor} ---")
    # .loc[] permite filtrar linhas com base em uma condição
    df_filtrado = df.loc[df[coluna] == valor]
    print(f"  Encontradas {len(df_filtrado)} linhas.")
    print(df_filtrado.to_string(index=False))
    return df_filtrado

# ============================================================
# 7. FUNÇÃO PARA ESTATÍSTICAS POR GRUPO
# ============================================================
def estatisticas_por_grupo(nome, df, coluna_grupo, coluna_valor):
    """
    Calcula estatísticas (soma, média, contagem) agrupadas
    por uma coluna.

    Parâmetros:
        nome (str): Nome do dataset
        df (pd.DataFrame): DataFrame
        coluna_grupo (str): Coluna para agrupar
        coluna_valor (str): Coluna numérica para calcular
    """
    if coluna_grupo not in df.columns or coluna_valor not in df.columns:
        print(f"  [AVISO] Colunas não encontradas no dataset '{nome}'")
        return None

    print(f"\n  --- Estatísticas de '{coluna_valor}' por '{coluna_grupo}' ---")

    # .groupby() agrupa os dados pela coluna especificada
    # .agg() aplica funções de agregação (soma, média, contagem)
    grupos = df.groupby(coluna_grupo)[coluna_valor].agg(
        ["sum", "mean", "count"]
    )

    # Renomear colunas para facilitar a leitura
    grupos.columns = ["Soma", "Media", "Contagem"]

    # Arredondar para 2 casas decimais
    grupos = grupos.round(2)

    # Ordenar pela soma (do maior para o menor)
    grupos = grupos.sort_values(by="Soma", ascending=False)

    print(grupos.to_string())
    return grupos

# ============================================================
# 8. PROGRAMA PRINCIPAL
# ============================================================
def main():
    """
    Função principal que executa todas as análises.
    É o ponto de entrada do programa.
    """
    print("\n" + "="*60)
    print("  ANÁLISE DE VENDAS - VAREJO DE MODA")
    print("  Projeto de Extensão - Faculdade Estácio de Sá")
    print("="*60)

    # --------------------------------------------------------
    # ETAPA 1: Ler todos os arquivos CSV
    # --------------------------------------------------------
    print("\n>>> ETAPA 1: Leitura dos arquivos CSV")
    dataframes = {}

    for nome, config in ARQUIVOS.items():
        df = ler_csv(nome, config)
        if df is not None:
            dataframes[nome] = df

    # --------------------------------------------------------
    # ETAPA 1.1: Converter colunas numéricas
    # --------------------------------------------------------
    # Os CSVs usam formato brasileiro (vírgula decimal, ponto de milhar)
    # Precisamos converter para o formato que o Python entende
    print("\n>>> ETAPA 1.1: Convertendo colunas numéricas...")

    # Converter colunas do dataset de vendas por mês/ano
    if "Vendas_Mes_Ano" in dataframes:
        colunas_numericas = ["Total custo", "Total venda", "Valor lucro", "%Lucro"]
        dataframes["Vendas_Mes_Ano"] = converter_colunas_numericas(
            dataframes["Vendas_Mes_Ano"], colunas_numericas
        )
        print("  [OK] Vendas_Mes_Ano convertido.")

    # Converter colunas do dataset de produtos
    if "Vendas_Produto" in dataframes:
        colunas_numericas = ["Total custo", "Total venda", "Valor lucro", "%Lucro"]
        dataframes["Vendas_Produto"] = converter_colunas_numericas(
            dataframes["Vendas_Produto"], colunas_numericas
        )
        print("  [OK] Vendas_Produto convertido.")

    # Converter colunas do dataset de clientes
    if "Vendas_Cliente" in dataframes:
        colunas_numericas = ["Subtotal ", "Descontos ", "Frete  ", "Total ", "Recebido ", "Troco "]
        dataframes["Vendas_Cliente"] = converter_colunas_numericas(
            dataframes["Vendas_Cliente"], colunas_numericas
        )
        print("  [OK] Vendas_Cliente convertido.")

    # Converter colunas do dataset de produtos detalhado
    if "Vendas_Produto_Detalhado" in dataframes:
        colunas_numericas = ["Total custo", "Total venda", "Valor lucro", "%Lucro"]
        dataframes["Vendas_Produto_Detalhado"] = converter_colunas_numericas(
            dataframes["Vendas_Produto_Detalhado"], colunas_numericas
        )
        print("  [OK] Vendas_Produto_Detalhado convertido.")

    # --------------------------------------------------------
    # ETAPA 2: Exibir informações gerais de cada dataset
    # --------------------------------------------------------
    print("\n>>> ETAPA 2: Informações gerais dos datasets")

    for nome, df in dataframes.items():
        exibir_info(nome, df)

    # --------------------------------------------------------
    # ETAPA 3: Ordenações nos dados
    # --------------------------------------------------------
    print("\n>>> ETAPA 3: Ordenações nos dados")

    # Ordenar vendas por mês/ano pelo valor de venda (maior primeiro)
    if "Vendas_Mes_Ano" in dataframes:
        print("\n  [Vendas_Mes_Ano] Top 10 meses com maior venda total:")
        ordenar_dados(
            "Vendas_Mes_Ano",
            dataframes["Vendas_Mes_Ano"],
            "Total venda",
            Crescente=False  # False = do maior para o menor
        )

    # Ordenar produtos por lucro (maior primeiro)
    if "Vendas_Produto" in dataframes:
        print("\n  [Vendas_Produto] Top 10 produtos com maior lucro:")
        ordenar_dados(
            "Vendas_Produto",
            dataframes["Vendas_Produto"],
            "Valor lucro",
            Crescente=False
        )

    # --------------------------------------------------------
    # ETAPA 4: Filtrar dados
    # --------------------------------------------------------
    print("\n>>> ETAPA 4: Filtros nos dados")

    # Filtrar vendas de 2024 no dataset de vendas por mês/ano
    if "Vendas_Mes_Ano" in dataframes:
        print("\n  Vendas do ano de 2024:")
        filtrar_dados(
            "Vendas_Mes_Ano",
            dataframes["Vendas_Mes_Ano"],
            "Ano",
            2024
        )

    # Filtrar vendas de 2025
    if "Vendas_Mes_Ano" in dataframes:
        print("\n  Vendas do ano de 2025:")
        filtrar_dados(
            "Vendas_Mes_Ano",
            dataframes["Vendas_Mes_Ano"],
            "Ano",
            2025
        )

    # --------------------------------------------------------
    # ETAPA 5: Estatísticas por grupo
    # --------------------------------------------------------
    print("\n>>> ETAPA 5: Estatísticas por grupo")

    # Vendas por ano
    if "Vendas_Mes_Ano" in dataframes:
        print("\n  Total de vendas por ano:")
        estatisticas_por_grupo(
            "Vendas_Mes_Ano",
            dataframes["Vendas_Mes_Ano"],
            "Ano",
            "Total venda"
        )

    # Vendas por cliente (dataset de clientes)
    if "Vendas_Cliente" in dataframes:
        print("\n  Total gasto por cliente (top 10):")
        estatisticas_por_grupo(
            "Vendas_Cliente",
            dataframes["Vendas_Cliente"],
            "Nome cliente ",
            "Total "
        )

    # --------------------------------------------------------
    # ETAPA 6: Resumo final
    # --------------------------------------------------------
    print("\n" + "="*60)
    print("  ANÁLISE INICIAL CONCLUÍDA!")
    print("="*60)
    print("\n  Próximos passos sugeridos:")
    print("    - Criar gráficos de barras e pizza")
    print("    - Analisar sazonalidade das vendas")
    print("    - Identificar produtos estrela e produtos problemáticos")
    print("    - Calcular margem de lucro por categoria")
    print("    - Analisar comportamento de compra dos clientes")
    print("    - Tentativa de commit no github feita pelo Northon")

# ============================================================
# 9. EXECUÇÃO DO PROGRAMA
# ============================================================
# Este trecho garante que a função main() só é chamada
# quando o script é executado diretamente (não quando é importado)
if __name__ == "__main__":
    main()
