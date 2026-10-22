"""
PI2 - Câmbio, crédito bancário e o Porto de Santos
Monta o painel de modelagem: o painel principal com a série de crédito sem o
Bradesco (`credito_ex_bradesco`), construída a partir do ESTBAN aberto por banco.

Por que existe: o degrau de agosto/2019 em `credito_total` vem quase todo de uma
única instituição (Bradesco). A decisão de usar o crédito dos demais bancos como
série principal da modelagem está justificada em `notebooks/10_estban_por_banco_degrau_2019.ipynb`.

Rode este script de dentro da pasta /src (ex.: `cd src && python build_modeling_panel.py`).

Entradas (em ../data/):
  - raw/estban_verbetes_santos_2015-2025_por_banco.csv  -> ESTBAN por banco e verbete
  - processed/painel_2015_2025.csv                      -> painel principal (merge_datasets.py)

Saída (em ../data/processed/):
  - painel_modelagem_2015_2025.csv
      132 meses. `credito_ex_bradesco` só existe de 2015-01 a 2024-12 (120 meses):
      em 2025 há buracos de reporte de bancos específicos (Itaú, Santander, Banco do
      Brasil), e somar os bancos que sobram criaria quedas artificiais no agregado.
"""

import pandas as pd

DATA = "../data/"
BRADESCO = "60746948"      # cnpj_basico de BCO BRADESCO S.A.
VERBETE_CREDITO = 160      # operações de crédito (mesmo verbete de `credito_total`)
ULTIMO_MES_SEM_BURACO = "2024-12-01"

por_banco = pd.read_csv(DATA + "raw/estban_verbetes_santos_2015-2025_por_banco.csv", dtype={"cnpj_basico": str})
por_banco["data"] = pd.to_datetime(dict(year=por_banco["ano"], month=por_banco["mes"], day=1))

credito = por_banco[(por_banco["id_verbete"] == VERBETE_CREDITO) & (por_banco["data"] <= ULTIMO_MES_SEM_BURACO)]
credito_ex = (
    credito[credito["cnpj_basico"] != BRADESCO]
    .groupby(["ano", "mes"], as_index=False)["valor_total"].sum()
    .rename(columns={"valor_total": "credito_ex_bradesco"})
)

painel = pd.read_csv(DATA + "processed/painel_2015_2025.csv")
colunas = ["ano", "mes", "cambio_venda", "credito_total", "exportação_fob", "importação_fob", "exportação_kg", "importação_kg"]
saida = painel[colunas].merge(credito_ex, on=["ano", "mes"], how="left")
saida.insert(4, "credito_ex_bradesco", saida.pop("credito_ex_bradesco"))

saida.to_csv(DATA + "processed/painel_modelagem_2015_2025.csv", index=False)
print(f"painel_modelagem_2015_2025.csv: {len(saida)} meses, "
      f"credito_ex_bradesco preenchido em {saida['credito_ex_bradesco'].notna().sum()} meses")
