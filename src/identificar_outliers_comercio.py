"""
PI2 - Câmbio, crédito bancário e o Porto de Santos
Identifica, dentro do painel mensal já processado, quais meses são outliers
(critério IQR, o mesmo usado na EDA) em alguma das variáveis de comércio
exterior. Esses são os meses candidatos a uma consulta pontual por produto
(NCM) no Comex Stat — não entram no painel principal, servem só pra apontar
ONDE vale a pena aprofundar com dado de produto.

Rode este script de dentro da pasta /src (ex.: `cd src && python identificar_outliers_comercio.py`).

Arquivo de entrada esperado (em ../data/processed/):
  - painel_2015_2025.csv

Saída (em ../data/processed/):
  - meses_outliers_comercio.csv -> lista de (ano, mes, variáveis que flagaram o mês)
"""

import pandas as pd

PROCESSED = "../data/processed/"

# variáveis de comércio exterior — só essas fazem sentido detalhar por NCM
# (câmbio, crédito e ativo/passivo não têm quebra por produto no Comex Stat)
COLUNAS_COMERCIO = ["exportação_fob", "importação_fob", "exportação_kg", "importação_kg"]


def identificar_meses_outliers_comercio(df, colunas=COLUNAS_COMERCIO):
    """Aplica o critério IQR (mesmo do boxplot da EDA: fora de Q1-1.5*IQR /
    Q3+1.5*IQR) em cada coluna de `colunas` e devolve um DataFrame com um mês
    por linha e quais variáveis flagaram aquele mês como atípico.

    Une os outliers das várias colunas: um mês que é outlier em mais de uma
    variável aparece uma vez só, com as duas variáveis listadas — assim o
    conjunto final é sempre a MENOR lista de meses que já justificaria uma
    consulta por produto, sem repetição.
    """
    flags = {}  # (ano, mes) -> lista de colunas que flagaram esse mês

    for col in colunas:
        serie = df[col].dropna()
        q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
        iqr = q3 - q1
        lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = serie[(serie < lo_fence) | (serie > hi_fence)]

        for idx in outliers.index:
            chave = (int(df.loc[idx, "ano"]), int(df.loc[idx, "mes"]))
            flags.setdefault(chave, []).append(col)

    if not flags:
        return pd.DataFrame(columns=["ano", "mes", "variaveis_outlier"])

    linhas = [
        {"ano": ano, "mes": mes, "variaveis_outlier": "; ".join(cols)}
        for (ano, mes), cols in flags.items()
    ]
    resultado = pd.DataFrame(linhas).sort_values(["ano", "mes"]).reset_index(drop=True)
    return resultado


if __name__ == "__main__":
    painel = pd.read_csv(PROCESSED + "painel_2015_2025.csv")
    meses_outliers = identificar_meses_outliers_comercio(painel)

    meses_outliers.to_csv(PROCESSED + "meses_outliers_comercio.csv", index=False)

    print(f"{len(meses_outliers)} mês(es) pedem detalhamento por produto no Comex Stat:")
    print()
    if len(meses_outliers) > 0:
        print(meses_outliers.to_string(index=False))
    else:
        print("(nenhum outlier nas variáveis de comércio exterior no recorte atual)")
    print()
    print(f"Lista salva em {PROCESSED}meses_outliers_comercio.csv")
