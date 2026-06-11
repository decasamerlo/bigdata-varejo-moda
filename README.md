# Estudo de Vendas, Custos e Margens de Lucro no Varejo de Moda

Projeto de Extensao da Faculdade Estacio de Sa - Campus Barreiros, Sao Jose/SC

## Integrantes

- **Northon Vinicius Cardoso** - Coleta dos dados
- **Andre Casagranda Merlo** - Analise e organizacao dos dados
- **Orientador:** Thiago Cunha

## Objetivo

Analisar dados reais de vendas de uma loja de roupas de pequeno porte para:
- Identificar produtos mais lucrativos
- Comparar custos, vendas e lucros
- Gerar visualizacoes graficas para tomada de decisao

## Estrutura do Projeto

```
Trab/
├── analise_vendas.py          # Script principal de analise
├── Total-Vendas-Mes-Ano.csv   # Vendas mensais por ano (2011-2026)
├── Total-Vendas-Produto.csv   # Cadastro de produtos com custo/venda/lucro
├── Vendas-Cliente-2024-2025.csv     # Vendas por cliente (2024-2025)
├── Vendas-Produto-2024-2025.csv     # Vendas detalhadas por produto
├── ROTEIRO_DE_EXTENSAO.docx   # Roteiro do projeto
├── ROTEIRO_DE_EXTENSAO.pdf    # Roteiro do projeto (PDF)
├── ROTEIRO_DE_EXTENSAO.txt    # Roteiro do projeto (texto)
└── README.md                  # Este arquivo
```

## Requisitos

- Python 3.10+
- pandas

## Como Executar

```bash
# Instalar dependencias (se necessario)
pip install pandas

# Executar o script
python3 analise_vendas.py
```

## Funcionalidades do Script

1. **Leitura dos CSVs** - Carrega todos os arquivos de dados
2. **Conversao de tipos** - Trata formato brasileiro (virgula decimal, ponto de milhar)
3. **Informacoes gerais** - Dimensoes, colunas, tipos, estatisticas
4. **Ordenacao** - Top vendas, top lucros
5. **Filtros** - Vendas por ano
6. **Agregacoes** - Totais por ano, gastos por cliente

## Sobre os Dados

| Arquivo | Registros | Descricao |
|---------|-----------|-----------|
| Vendas_Mes_Ano | 192 | Resumo mensal de vendas (jan/2011 - jul/2026) |
| Vendas_Produto | 9.186 | Cadastro de produtos com margens de lucro |
| Vendas_Cliente | 274 | Vendas individuais por cliente (2024-2025) |
| Vendas_Produto_Detalhado | 552 | Vendas detalhadas por produto (2024-2025) |
