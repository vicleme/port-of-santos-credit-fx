# port-santos-credit-fx

**🇺🇸 [Read this in English](README.md)**

Análise da relação entre variação cambial, crédito bancário e movimentação de carga no Porto de Santos (2015–2025), usando dados abertos do Banco Central do Brasil (BCB) e da estatística portuária. Projeto de ciência de dados — Fatec Baixada Santista.


## Tema

Relação entre variação cambial, crédito bancário e movimentação de carga no Porto de Santos: uma análise de dados públicos do Banco Central e da Autoridade Portuária (2015–2025).

## Objetivo geral

Investigar, por meio de dados públicos, se há relação estatística entre a variação da taxa de câmbio, o volume de crédito bancário direcionado a atividades de comércio exterior e logística no município de Santos, e a movimentação de carga no Porto de Santos, no período de 2015 a 2025.

## Estrutura do repositório

```
data/
  raw/          -> dados brutos, como baixados das fontes originais
  processed/    -> painel mensal já tratado e pronto para análise
notebooks/      -> EDA e análises estatísticas
src/            -> scripts reutilizáveis (ex.: merge_datasets.py)
docs/           -> rascunhos do relatório, atas de reunião do grupo
```

## Fontes de dados

| Arquivo (`data/raw/`) | Fonte | Cobertura | Observações |
|---|---|---|---|
| `cambio_sgs_3696_2015-2026.csv` | BCB — SGS, série 3696 (Taxa de câmbio, Livre, Dólar americano, venda, fim de período, mensal) | 2015-01 a 2026-07 | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.3696/dados` |
| `estban_credito_santos_2015-2025.csv` | BCB — ESTBAN, via Base dos Dados (`basedosdados.br_bcb_estban.municipio`), município de Santos (IBGE 3548500) | 2015-01 a 2025-09 (plano gratuito) | Formato longo, um registro por (ano, mês, verbete). Verbetes usados: 160/161/162/171 (crédito) e 399/899 (totais ativo/passivo). Verbetes 153/457 (carteira de câmbio) testados e descartados — retornaram nulos/zerados, provável supressão por sigilo estatístico. |
| `comexstat_porto_santos_2015-2026.csv` | Comex Stat — MDIC, módulo "Geral", filtro Via=Marítima + URF=0817800 (Porto de Santos) | 2015-01 a 2026-07 | Módulo "Geral" usado em vez de "Municípios" para captar o fluxo físico pela alfândega, não o domicílio fiscal do exportador/importador. |

## Dados processados (`data/processed/`)

- **`painel_2015_2025.csv`** — painel mensal principal, recorte fechado no escopo formal do projeto (2015–2025). 132 meses, 13 colunas. Usar este para a análise do PI2.
- **`painel_completo.csv`** — mesmo painel, sem corte, incluindo os meses extras de 2026 já baixados de câmbio e Comex Stat (ESTBAN fica vazio nesses meses). Guardado como dado extra para eventual extensão futura (ex.: PI4).

## Como reproduzir

```bash
cd src
python merge_datasets.py
```

Gera `painel_completo.csv` e `painel_2015_2025.csv` em `data/processed/` a partir dos arquivos brutos em `data/raw/`.

## Licença

Code is licensed under MIT (see LICENSE). Written analysis and report content are licensed under CC BY 4.0.

Os dados brutos em `data/raw/` continuam sujeitos aos termos de dados abertos das respectivas fontes originais (BCB, MDIC) — a licença deste repositório cobre o código e a análise produzidos pelo grupo, não os dados de origem.
