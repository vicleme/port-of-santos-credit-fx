# port-santos-credit-fx

**🇧🇷 [Leia isto em Português](README.pt-br.md)**

Analysis of the relationship between exchange rate volatility, bank credit, and cargo volume at the Port of Santos (2015–2025), using open data from Brazil's Central Bank (BCB) and port authority statistics. Data science project — Fatec Baixada Santista.

## Topic

Relationship between exchange rate variation, bank credit, and cargo movement at the Port of Santos: an analysis of public data from the Central Bank and the Port Authority (2015–2025).

## General objective

To investigate, using public data, whether there is a statistical relationship between exchange rate variation, the volume of bank credit directed to foreign trade and logistics activities in the municipality of Santos, and cargo movement at the Port of Santos, over the period 2015–2025.

## Repository structure

```
data/
  raw/          -> raw data, as downloaded from the original sources
  processed/    -> monthly panel already cleaned and ready for analysis
notebooks/      -> EDA and statistical analysis
src/            -> reusable scripts (e.g., merge_datasets.py)
docs/           -> report drafts, group meeting notes
```

## Data sources

| File (`data/raw/`) | Source | Coverage | Notes |
|---|---|---|---|
| `cambio_sgs_3696_2015-2026.csv` | BCB — SGS, series 3696 (Exchange rate, Free market, US Dollar, sell, end of period, monthly) | 2015-01 to 2026-07 | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.3696/dados` |
| `estban_credito_santos_2015-2025.csv` | BCB — ESTBAN, via Base dos Dados (`basedosdados.br_bcb_estban.municipio`), municipality of Santos (IBGE 3548500) | 2015-01 to 2025-09 (free tier) | Long format, one record per (year, month, account code). Account codes used: 160/161/162/171 (credit) and 399/899 (total assets/liabilities). Account codes 153/457 (foreign exchange portfolio) were tested and dropped — returned null/zero values, likely due to statistical confidentiality suppression. |
| `comexstat_porto_santos_2015-2026.csv` | Comex Stat — MDIC, "General" module, filtered by Transport mode=Maritime + Customs unit=0817800 (Port of Santos) | 2015-01 to 2026-07 | The "General" module was used instead of "Municipalities" to capture the physical flow through customs, rather than the exporter/importer's tax domicile. |

## Processed data (`data/processed/`)

- **`painel_2015_2025.csv`** — main monthly panel, closed to the project's formal scope (2015–2025). 132 months, 13 columns. Use this one for the PI2 analysis.
- **`painel_completo.csv`** — same panel, unclipped, including the extra 2026 months already downloaded for exchange rate and Comex Stat (ESTBAN is empty for those months). Kept as extra data for a possible future extension (e.g., a follow-up project).

## How to reproduce

```bash
cd src
python merge_datasets.py
```

Generates `painel_completo.csv` and `painel_2015_2025.csv` in `data/processed/` from the raw files in `data/raw/`.

## License

Code is licensed under MIT (see LICENSE). Written analysis and report content are licensed under CC BY 4.0.

The raw data in `data/raw/` remains subject to the open data terms of the original sources (BCB, MDIC) — this repository's license covers the code and analysis produced by the group, not the source data.
