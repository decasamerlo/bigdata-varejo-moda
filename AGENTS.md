# AGENTS.md

## Project Overview

Academic extension project analyzing retail clothing sales data (Brazilian store). Single Python script + CSV data files.

## Quick Start

```bash
pip install pandas
python3 analise_vendas.py
```

## Key Facts

- **Language:** Python 3.10+
- **Dependencies:** pandas (only)
- **Data format:** CSV files use Brazilian number formatting (comma as decimal separator, period as thousand separator)
- **Separators vary:** Most CSVs use `,` but `Vendas-Cliente-2024-2025.csv` uses `;`
- **Encoding:** latin-1 (not UTF-8) — required for accented characters

## Conventions

- Script comments are in Portuguese (Brazilian)
- All data processing in single file `analise_vendas.py`
- No tests, no linting, no CI — academic project
