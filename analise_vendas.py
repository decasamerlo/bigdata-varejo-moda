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

# matplotlib é a biblioteca mais usada para criar gráficos em Python
import matplotlib
matplotlib.use("TkAgg")  # Força o uso do backend TkAgg para gráficos
import matplotlib.pyplot as plt

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
            encoding="UTF*-8"  # Tente UTF-8 primeiro, se der erro, use 'latin-1'
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

    # Itera sobre o dicionário de arquivos, lendo cada um e armazenando
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
    # ETAPA 6: Gráficos
    # --------------------------------------------------------
    print("\n>>> ETAPA 6: Gráficos")

    def gerar_todos_graficos(dataframes):
        """
        Gera todos os gráficos de análise de vendas.
        Parâmetros:
            dataframes (dict): Dicionário com os DataFrames carregados
        """
    
        # Paleta de cores padrão para os gráficos
        COR_CUSTO    = "#E07B54"   # laranja
        COR_VENDA    = "#4A90D9"   # azul
        COR_LUCRO    = "#5BAD72"   # verde
        COR_DESTAQUE = "#F5C842"   # amarelo
        CORES_MULTI  = ["#4A90D9", "#5BAD72", "#E07B54", "#9B59B6",
                        "#F5C842", "#1ABC9C", "#E74C3C", "#2ECC71"]
    
        # --------------------------------------------------------
        # BLOCO 1 — Total-Vendas-Mes-Ano.csv
        # --------------------------------------------------------
        if "Vendas_Mes_Ano" in dataframes:
            df = dataframes["Vendas_Mes_Ano"].copy()
    
            # Cria um rótulo "Mês/Ano" para o eixo X
            df["Periodo"] = df["Mês"].astype(str) + "/" + df["Ano"].astype(str)
    
            # ── Gráfico 1.1: Linha — Tendência de vendas ao longo do tempo ──
            fig, ax = plt.subplots(figsize=(14, 5))
            ax.plot(df["Periodo"], df["Total venda"],
                    marker="o", color=COR_VENDA, linewidth=2, label="Total Venda")
            ax.set_title("Tendência de Vendas por Mês/Ano", fontsize=14, fontweight="bold")
            ax.set_xlabel("Período (Mês/Ano)")
            ax.set_ylabel("Total de Vendas (R$)")
            ax.tick_params(axis="x", rotation=45)
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_1_1_tendencia_vendas.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 1.1 gerado.")
    
            # ── Gráfico 1.2: Barras agrupadas — Custo vs Venda vs Lucro por mês ──
            x = range(len(df))
            largura = 0.28
            fig, ax = plt.subplots(figsize=(16, 6))
            ax.bar([i - largura for i in x], df["Total custo"],  width=largura, label="Custo",  color=COR_CUSTO)
            ax.bar([i           for i in x], df["Total venda"],  width=largura, label="Venda",  color=COR_VENDA)
            ax.bar([i + largura for i in x], df["Valor lucro"],  width=largura, label="Lucro",  color=COR_LUCRO)
            ax.set_xticks(list(x))
            ax.set_xticklabels(df["Periodo"], rotation=45, ha="right")
            ax.set_title("Custo vs Venda vs Lucro por Mês/Ano", fontsize=14, fontweight="bold")
            ax.set_ylabel("Valor (R$)")
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_1_2_custo_venda_lucro_mes.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 1.2 gerado.")
    
            # ── Gráfico 1.3: Barras empilhadas — Proporção custo e lucro no total ──
            fig, ax = plt.subplots(figsize=(14, 5))
            ax.bar(df["Periodo"], df["Total custo"], label="Custo",  color=COR_CUSTO)
            ax.bar(df["Periodo"], df["Valor lucro"], bottom=df["Total custo"],
                label="Lucro", color=COR_LUCRO)
            ax.set_title("Proporção Custo vs Lucro por Mês/Ano (Empilhado)", fontsize=14, fontweight="bold")
            ax.set_xlabel("Período (Mês/Ano)")
            ax.set_ylabel("Valor (R$)")
            ax.tick_params(axis="x", rotation=45)
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_1_3_empilhado_mes.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 1.3 gerado.")
    
            # ── Gráfico 1.4: Linha dupla — %Lucro vs Total Venda ──
            fig, ax1 = plt.subplots(figsize=(14, 5))
            ax2 = ax1.twinx()  # segundo eixo Y
    
            ax1.plot(df["Periodo"], df["Total venda"],
                    marker="o", color=COR_VENDA, linewidth=2, label="Total Venda")
            ax2.plot(df["Periodo"], df["%Lucro"],
                    marker="s", color=COR_DESTAQUE, linewidth=2, linestyle="--", label="% Lucro")
    
            ax1.set_xlabel("Período (Mês/Ano)")
            ax1.set_ylabel("Total Venda (R$)", color=COR_VENDA)
            ax2.set_ylabel("% Lucro", color=COR_DESTAQUE)
            ax1.tick_params(axis="x", rotation=45)
    
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    
            ax1.set_title("Evolução do % de Lucro vs Total de Vendas", fontsize=14, fontweight="bold")
            ax1.grid(True, linestyle="--", alpha=0.4)
            plt.tight_layout()
            plt.savefig("grafico_1_4_pct_lucro_vs_venda.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 1.4 gerado.")
    
        # --------------------------------------------------------
        # BLOCO 2 — Total-Vendas-Produto.csv
        # --------------------------------------------------------
        if "Vendas_Produto" in dataframes:
            df = dataframes["Vendas_Produto"].copy()
    
            # Descobre o nome da coluna de produto automaticamente
            col_produto = df.columns[0]
    
            # ── Gráfico 2.1: Barras horizontais — Ranking produtos mais lucrativos ──
            df_ord = df.sort_values("Valor lucro", ascending=True).tail(15)
            fig, ax = plt.subplots(figsize=(12, 7))
            bars = ax.barh(df_ord["Nome"], df_ord["Valor lucro"], color=COR_LUCRO)
            ax.bar_label(bars, fmt="R$ %.0f", padding=4, fontsize=8)
            ax.set_title("Top 15 Produtos Mais Lucrativos", fontsize=14, fontweight="bold")
            ax.set_xlabel("Valor de Lucro (R$)")
            ax.grid(axis="x", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_2_1_ranking_lucro_produto.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 2.1 gerado.")
    
            # ── Gráfico 2.3: Barras agrupadas — Custo vs Venda por produto (top 10) ──
            df_top = df.sort_values("Total venda", ascending=False).head(10)
            x = range(len(df_top))
            largura = 0.35
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.bar([i - largura/2 for i in x], df_top["Total custo"], width=largura,
                label="Custo", color=COR_CUSTO)
            ax.bar([i + largura/2 for i in x], df_top["Total venda"], width=largura,
                label="Venda", color=COR_VENDA)
            ax.set_xticks(list(x))
            ax.set_xticklabels(df_top["Nome"], rotation=30, ha="right")
            ax.set_title("Custo vs Venda — Top 10 Produtos", fontsize=14, fontweight="bold")
            ax.set_ylabel("Valor (R$)")
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_2_3_custo_venda_produto.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 2.3 gerado.")
    
            # ── Gráfico 2.4: Pizza — Participação de cada produto no lucro total ──
            df_top_pizza = df.sort_values("Valor lucro", ascending=False).head(8)
            outros = df["Valor lucro"].sum() - df_top_pizza["Valor lucro"].sum()
            if outros > 0:
                outros_row = {col_produto: "Outros", "Valor lucro": outros}
                df_top_pizza = pd.concat(
                    [df_top_pizza, pd.DataFrame([outros_row])], ignore_index=True
                )
            fig, ax = plt.subplots(figsize=(10, 7))
            ax.pie(
                df_top_pizza["Valor lucro"],
                labels=df_top_pizza[col_produto],
                autopct="%1.1f%%",
                colors=CORES_MULTI[:len(df_top_pizza)],
                startangle=140
            )
            ax.set_title("Participação dos Produtos no Lucro Total", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig("grafico_2_4_pizza_lucro_produto.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 2.4 gerado.")
    
        # --------------------------------------------------------
        # BLOCO 3 — Vendas-Cliente-2024-2025.csv
        # --------------------------------------------------------
        if "Vendas_Cliente" in dataframes:
            df = dataframes["Vendas_Cliente"].copy()
    
            # Descobre a coluna de nome do cliente (tira espaços extras)
            df.columns = df.columns.str.strip()
            col_cliente = [c for c in df.columns if "cliente" in c.lower() or "nome" in c.lower()][0]
            col_total   = [c for c in df.columns if "total" in c.lower()][0]
            col_desc    = [c for c in df.columns if "desconto" in c.lower()][0]
    
            # ── Gráfico 3.1: Barras horizontais — Clientes que mais gastaram ──
            df_cli = df.groupby(col_cliente)[col_total].sum().sort_values(ascending=True).tail(15)
            fig, ax = plt.subplots(figsize=(12, 7))
            bars = ax.barh(df_cli.index, df_cli.values, color=COR_VENDA)
            ax.bar_label(bars, fmt="R$ %.0f", padding=4, fontsize=8)
            ax.set_title("Top 15 Clientes por Total Gasto", fontsize=14, fontweight="bold")
            ax.set_xlabel("Total Gasto (R$)")
            ax.grid(axis="x", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_3_1_ranking_clientes.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 3.1 gerado.")
    
            # ── Gráfico 3.2: Barras — Desconto total por cliente (top 10) ──
            df_desc = df.groupby(col_cliente)[col_desc].sum().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.bar(df_desc.index, df_desc.values, color=COR_DESTAQUE)
            ax.set_title("Top 10 Clientes com Maior Desconto Acumulado", fontsize=14, fontweight="bold")
            ax.set_xlabel("Cliente")
            ax.set_ylabel("Total de Descontos (R$)")
            ax.tick_params(axis="x", rotation=30)
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_3_2_desconto_cliente.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 3.2 gerado.")
    
            # ── Gráfico 3.3: Histograma — Distribuição do ticket médio ──
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(df[col_total].dropna(), bins=20, color=COR_LUCRO, edgecolor="white")
            ax.set_title("Distribuição dos Valores de Compra (Ticket)", fontsize=14, fontweight="bold")
            ax.set_xlabel("Valor da Compra (R$)")
            ax.set_ylabel("Frequência")
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.savefig("grafico_3_3_histograma_ticket.png", dpi=150)
            plt.show()
            print("  [OK] Gráfico 3.3 gerado.")
    
        # --------------------------------------------------------
        # BLOCO 4 — Vendas-Produto-2024-2025.csv
        # --------------------------------------------------------
        if "Vendas_Produto_Detalhado" in dataframes:
            df = dataframes["Vendas_Produto_Detalhado"].copy()
    
            col_produto = df.columns[0]
    
            # Verifica se tem coluna de ano para comparação 2024 vs 2025
            tem_ano = "Ano" in df.columns
    
            if tem_ano:
                # ── Gráfico 4.1: Barras agrupadas — 2024 vs 2025 por produto (top 10) ──
                df_pivot = df.groupby([col_produto, "Ano"])["Total venda"].sum().unstack(fill_value=0)
                df_pivot = df_pivot.sort_values(
                    by=df_pivot.columns[-1], ascending=False
                ).head(10)
    
                x = range(len(df_pivot))
                largura = 0.35
                anos = df_pivot.columns.tolist()
                fig, ax = plt.subplots(figsize=(14, 6))
                for i, ano in enumerate(anos):
                    offset = (i - len(anos)/2 + 0.5) * largura
                    ax.bar([xi + offset for xi in x], df_pivot[ano],
                        width=largura, label=str(ano),
                        color=CORES_MULTI[i % len(CORES_MULTI)])
                ax.set_xticks(list(x))
                ax.set_xticklabels(df_pivot.index, rotation=30, ha="right")
                ax.set_title("Vendas por Produto: 2024 vs 2025 (Top 10)", fontsize=14, fontweight="bold")
                ax.set_ylabel("Total Venda (R$)")
                ax.legend(title="Ano")
                ax.grid(axis="y", linestyle="--", alpha=0.5)
                plt.tight_layout()
                plt.savefig("grafico_4_1_produto_2024_2025.png", dpi=150)
                plt.show()
                print("  [OK] Gráfico 4.1 gerado.")
    
            # ── Gráfico 4.2: Linha — Evolução de vendas do produto mais lucrativo ──
            if tem_ano and "Mês" in df.columns:
                produto_top = df.groupby(col_produto)["Valor lucro"].sum().idxmax()
                df_prod = df[df[col_produto] == produto_top].copy()
                df_prod["Periodo"] = df_prod["Mês"].astype(str) + "/" + df_prod["Ano"].astype(str)
                df_prod = df_prod.sort_values(["Ano", "Mês"])
    
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(df_prod["Periodo"], df_prod["Total venda"],
                        marker="o", color=COR_VENDA, linewidth=2)
                ax.set_title(f"Evolução de Vendas — {produto_top}", fontsize=13, fontweight="bold")
                ax.set_xlabel("Período")
                ax.set_ylabel("Total Venda (R$)")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(True, linestyle="--", alpha=0.4)
                plt.tight_layout()
                plt.savefig("grafico_4_2_evolucao_produto_top.png", dpi=150)
                plt.show()
                print("  [OK] Gráfico 4.2 gerado.")
    
            # ── Gráfico 4.3: Heatmap — Volume de vendas por produto x mês ──
            if "Mês" in df.columns:
                df_heat = df.groupby([col_produto, "Mês"])["Total venda"].sum().unstack(fill_value=0)
                # Limita aos 12 produtos mais vendidos para não poluir
                df_heat = df_heat.loc[
                    df_heat.sum(axis=1).sort_values(ascending=False).head(12).index
                ]
    
                fig, ax = plt.subplots(figsize=(14, 7))
                im = ax.imshow(df_heat.values, aspect="auto", cmap="YlGn")
    
                ax.set_xticks(range(len(df_heat.columns)))
                ax.set_xticklabels([f"Mês {m}" for m in df_heat.columns])
                ax.set_yticks(range(len(df_heat.index)))
                ax.set_yticklabels(df_heat.index, fontsize=8)
    
                plt.colorbar(im, ax=ax, label="Total Venda (R$)")
                ax.set_title("Heatmap: Vendas por Produto x Mês", fontsize=14, fontweight="bold")
                plt.tight_layout()
                plt.savefig("grafico_4_3_heatmap_produto_mes.png", dpi=150)
                plt.show()
                print("  [OK] Gráfico 4.3 gerado.")
    
        print("\n  [CONCLUÍDO] Todos os gráficos foram gerados e salvos como .png.")

    gerar_todos_graficos(dataframes)
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
    print("    - Commit e branchNorthon criada")
# ============================================================
# 9. EXECUÇÃO DO PROGRAMA
# ============================================================
# Este trecho garante que a função main() só é chamada
# quando o script é executado diretamente (não quando é importado)
if __name__ == "__main__":
    main()

    
