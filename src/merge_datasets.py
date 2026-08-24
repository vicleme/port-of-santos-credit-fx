"""
PI2 - Câmbio, crédito bancário e o Porto de Santos
Junta as 3 fontes (SGS/câmbio, ESTBAN/crédito, Comex Stat/carga) num painel
mensal único: uma linha por (ano, mês), pronta para análise estatística.

Rode este script de dentro da pasta /src (ex.: `cd src && python merge_datasets.py`).

Arquivos de entrada esperados (em ../data/raw/):
  - cambio_sgs_3696_2015-2026.csv          -> câmbio (PTAX venda, mensal)
  - estban_credito_santos_2015-2025.csv    -> ESTBAN (crédito, formato longo)
  - comexstat_porto_santos_2015-2026.csv   -> Comex Stat (carga)

Saída (em ../data/processed/):
  - painel_completo.csv     -> tudo que os dados cobrirem (até jul/2026 no câmbio/Comex)
  - painel_2015_2025.csv    -> recorte fechado no escopo formal do PI2 (2015-2025)
"""

import pandas as pd

RAW = "../data/raw/"
PROCESSED = "../data/processed/"

# ---------------------------------------------------------------------------
# 1. CÂMBIO (SGS 3696 - PTAX venda, fim de período, mensal)
# ---------------------------------------------------------------------------
cambio = pd.read_csv(RAW + "cambio_sgs_3696_2015-2026.csv", sep=";", encoding="utf-8")
cambio["data"] = pd.to_datetime(cambio["data"], format="%d/%m/%Y")
cambio["valor"] = cambio["valor"].str.replace(",", ".").astype(float)
cambio["ano"] = cambio["data"].dt.year
cambio["mes"] = cambio["data"].dt.month
cambio = cambio.rename(columns={"valor": "cambio_venda"})[["ano", "mes", "cambio_venda"]]

# ---------------------------------------------------------------------------
# 2. ESTBAN (crédito bancário - formato longo -> largo)
# ---------------------------------------------------------------------------
estban_long = pd.read_csv(RAW + "estban_credito_santos_2015-2025.csv")
estban_long["id_verbete"] = estban_long["id_verbete"].astype(str)

nomes_verbete = {
    "160": "credito_total",
    "161": "credito_emprestimos_titulos",
    "162": "credito_financiamentos",
    "171": "credito_outras_operacoes",
    "399": "ativo_total",
    "899": "passivo_total",
}
estban_long["verbete_nome"] = estban_long["id_verbete"].map(nomes_verbete)

estban = estban_long.pivot_table(
    index=["ano", "mes"], columns="verbete_nome", values="valor_total", aggfunc="sum"
).reset_index()
estban["ano"] = estban["ano"].astype(int)
estban["mes"] = estban["mes"].astype(int)

# ---------------------------------------------------------------------------
# 3. COMEX STAT (movimentação de carga - Porto de Santos, Via Marítima)
# ---------------------------------------------------------------------------
comex_raw = pd.read_csv(
    RAW + "comexstat_porto_santos_2015-2026.csv",
    sep=";",
    encoding="utf-8-sig",
)
# limpar espaços/quebras de linha escondidas dentro dos campos
for col in comex_raw.columns:
    if comex_raw[col].dtype == object:
        comex_raw[col] = comex_raw[col].astype(str).str.strip().str.replace("\r", "", regex=False)
comex_raw.columns = [c.strip() for c in comex_raw.columns]

comex_raw["ano"] = comex_raw["Ano"].astype(int)
comex_raw["mes"] = comex_raw["Mês"].str.extract(r"^(\d+)").astype(int)
comex_raw["fluxo"] = comex_raw["Fluxo"].str.lower().str.strip()
comex_raw["fob"] = comex_raw["Valor US$ FOB"].astype(float)
comex_raw["kg"] = comex_raw["Quilograma Líquido"].astype(float)

comex_wide = comex_raw.pivot_table(
    index=["ano", "mes"], columns="fluxo", values=["fob", "kg"], aggfunc="sum"
)
comex_wide.columns = [f"{fluxo}_{metrica}" for metrica, fluxo in comex_wide.columns]
comex_wide = comex_wide.reset_index()
comex_wide["ano"] = comex_wide["ano"].astype(int)
comex_wide["mes"] = comex_wide["mes"].astype(int)

# ---------------------------------------------------------------------------
# 4. MERGE FINAL
# ---------------------------------------------------------------------------
painel = cambio.merge(estban, on=["ano", "mes"], how="outer")
painel = painel.merge(comex_wide, on=["ano", "mes"], how="outer")
painel = painel.sort_values(["ano", "mes"]).reset_index(drop=True)

painel.to_csv(PROCESSED + "painel_completo.csv", index=False)

# recorte fechado no escopo formal do PI2 (2015-2025)
painel_2015_2025 = painel[(painel["ano"] >= 2015) & (painel["ano"] <= 2025)]
painel_2015_2025.to_csv(PROCESSED + "painel_2015_2025.csv", index=False)

# ---------------------------------------------------------------------------
# 5. RESUMO
# ---------------------------------------------------------------------------
print("Painel completo:", painel.shape[0], "linhas x", painel.shape[1], "colunas")
print("Período:", painel["ano"].min(), "-", painel["ano"].max())
print()
print("Painel 2015-2025:", painel_2015_2025.shape[0], "linhas")
print()
print("Colunas nulas (contagem) no recorte 2015-2025:")
print(painel_2015_2025.isna().sum())
print()
print("Amostra (5 primeiras linhas):")
print(painel_2015_2025.head())
