# port-santos-credit-fx

**🇺🇸 [Read this in English](README.md)**

Análise da relação entre variação cambial, crédito bancário e movimentação de carga no Porto de Santos (2015–2025), usando dados abertos do Banco Central do Brasil (BCB) e da estatística portuária. Projeto de Ciência de Dados — Fatec Baixada Santista.


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
docs/           -> dicionário de dados (md/pdf/tex), roteiro da EDA e texto escrito (docs/artigo/)
```

## Fontes de dados

| Arquivo (`data/raw/`) | Fonte | Cobertura | Observações |
|---|---|---|---|
| `cambio_sgs_3696_2015-2026.csv` | BCB — SGS, série 3696 (Taxa de câmbio, Livre, Dólar americano, venda, fim de período, mensal) | 2015-01 a 2026-07 | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.3696/dados` |
| `estban_credito_santos_2015-2025.csv` | BCB — ESTBAN, via Base dos Dados (`basedosdados.br_bcb_estban.municipio`), município de Santos (IBGE 3548500) | 2015-01 a 2025-09 (plano gratuito) | Formato longo, um registro por (ano, mês, verbete). Verbetes usados: 160/161/162/171 (crédito) e 399/899 (totais ativo/passivo). Verbetes 153/457 (carteira de câmbio) testados e descartados — retornaram nulos/zerados, provável supressão por sigilo estatístico. |
| `comexstat_porto_santos_2015-2026.csv` | Comex Stat — MDIC, módulo "Geral", filtro Via=Marítima + URF=0817800 (Porto de Santos) | 2015-01 a 2026-07 | Módulo "Geral" usado em vez de "Municípios" para captar o fluxo físico pela alfândega, não o domicílio fiscal do exportador/importador. |
| `estban_agencias_santos_2015-2025.csv` | BCB — ESTBAN, via Base dos Dados (`basedosdados.br_bcb_estban.municipio`), município de Santos (IBGE 3548500) | 2015-01 a 2025-12 | Número de agências bancárias reportando em Santos por mês (soma de `agencias_processadas`, deduplicada por banco). Usado em `notebooks/03_agencias_ativo_credito.ipynb` para testar a hipótese de que o fechamento de agências explica o padrão de `ativo_total`/`credito_total`. |
| `estban_agencias_santos_2015-2025_por_banco.csv` | Mesma fonte, aberta por banco (`cnpj_basico`, `instituicao`) | 2015-01 a 2025-12 | Agências reportando por banco e mês. Usado no diagnóstico de que a instabilidade da série agregada de 2025 é problema de qualidade de dado (buraco de reporte de bancos específicos: Itaú, Santander e Banco do Brasil), não fechamento real de agência, e de que nenhum ano anterior tem esse problema. Ver `notebooks/03_agencias_ativo_credito.ipynb`, seção 3. |
| `estban_verbetes_santos_2015-2025_por_banco.csv` | Mesma fonte, verbetes 160/161/162/171/399/899 abertos por banco | 2015-01 a 2025-12 | Crédito e ativo por banco e mês (12 instituições, 6.564 linhas). Usado em `notebooks/10_estban_por_banco_degrau_2019.ipynb` para mostrar que o degrau de agosto/2019 do `credito_total` se concentra em um banco (Bradesco) e para construir a série de crédito dos modelos. A soma dos bancos reproduz exatamente o `estban_credito_santos_2015-2025.csv`. Sete pares banco-mês de 2025 têm valor ausente (buracos de reporte). |
| `comexstat_ncm_santos_2021-09_10.csv` | Comex Stat, MDIC, mesmos filtros acima, aberto por código NCM | 2021-09 e 2021-10 | Detalhe por produto do outlier de importação (recorde de `importação_kg`). Usado em `notebooks/02_outlier_importacao_2021.ipynb`. |

## Dados processados (`data/processed/`)

- **`painel_2015_2025.csv`** — painel mensal principal, recorte fechado no escopo formal do projeto (2015–2025). 132 meses, 13 colunas. Usar este para a análise do PI2.
- **`painel_2015_2026.csv`** — mesmo painel, sem corte, incluindo os meses extras de 2026 já baixados de câmbio e Comex Stat (ESTBAN fica vazio nesses meses). Guardado como dado extra para eventual extensão futura.
- **`painel_modelagem_2015_2025.csv`** — o painel principal mais `credito_ex_bradesco` (crédito dos demais bancos com agência em Santos, sem o Bradesco). A coluna nova só é preenchida de 2015-01 a 2024-12 (120 meses), porque 2025 tem buracos de reporte por banco. Gerado por `src/build_modeling_panel.py`; usado nos notebooks 11 e 12.

## Roteiro da EDA e notebooks

A análise exploratória segue um roteiro de 6 passos, documentado em [`docs/02_roteiro_eda.md`](docs/02_roteiro_eda.md). O número do notebook segue a **ordem de criação**, não o número do passo; a tabela abaixo mostra a correspondência.

| Notebook | Passo | O que faz |
|---|---|---|
| `01_eda_painel_2015_2025.ipynb` | 1. Univariada | Histograma/boxplot de cada série; localiza outliers. |
| `02_outlier_importacao_2021.ipynb` | Extensão do 1 | Detalha por produto (NCM) o outlier de importação de set-out/2021. |
| `03_agencias_ativo_credito.ipynb` | Extensão do 1 | Testa se o fechamento de agências bancárias em Santos explica o padrão de `ativo_total`/`credito_total`. |
| `04_temporal_painel_2015_2025.ipynb` | 2. Temporal | Evolução de cada série no tempo e sazonalidade por mês do calendário. |
| `05_tratamento_nans.ipynb` | 3. Tratamento dos NaNs | Onde estão os NaNs (só colunas ESTBAN, out-dez/2025) e por que são descartados em vez de interpolados. |
| `06_correlacao.ipynb` | 4. Correlação | Matriz de correlação sobre os níveis (primeiro indício, não prova). |
| `07_estacionariedade.ipynb` | 5. Estacionariedade | Teste de Dickey-Fuller aumentado (ADF) em cada série, em nível e em primeira diferença. |
| `08_decomposicao.ipynb` | 6. Decomposição | Tendência, sazonalidade e resíduo de `cambio_venda` e `exportação_fob`. |
| `09_correlacao_diferenciada.ipynb` | Extensão do 4 | Refaz a correlação em primeira diferença, com testes de significância e correlação cruzada (defasagens). |
| `10_estban_por_banco_degrau_2019.ipynb` | Modelagem, parte 1 | Abre o ESTBAN por banco: o degrau de agosto/2019 se concentra no Bradesco. Teste de Zivot e Andrews, comparação de quatro formas de usar o crédito e amostra de modelagem. |
| `11_log_estacionariedade_correlacao.ipynb` | Modelagem, parte 2 | ADF e correlação nas séries em logaritmo, agora com o crédito sem o Bradesco (as quatro séries são I(1)). |
| `12_cointegracao_granger.ipynb` | Modelagem, parte 3 | Cointegração (Engle-Granger e Johansen) e causalidade de Granger em um VAR de primeiras diferenças dos logs, com Toda e Yamamoto como verificação. |

As perguntas em aberto que a EDA quantitativa não responde (por exemplo, a causa do degrau de agosto/2019 e o motivo da mudança de patamar do câmbio em 2020) estão listadas em `docs/02_roteiro_eda.md`.

## Em que ponto a análise está

- As correlações entre câmbio, exportação e importação são fortes em nível e quase desaparecem em primeira diferença: boa parte do que se vê em nível é tendência compartilhada (notebooks 06, 07 e 09).
- O degrau de agosto/2019 no `credito_total` se concentra em um banco, sem mudança no número de agências, o que aponta para artefato de reporte. A causa não está documentada publicamente e foi consultada ao Banco Central (notebook 10). O crédito sem o Bradesco é a série de crédito dos modelos.
- A cointegração não está estabelecida de forma robusta, e o Granger não mostra precedência preditiva estável do câmbio ou do crédito sobre a carga (notebooks 11 e 12). Isso não prova ausência de relação, e Granger é previsão, não causalidade.
- O crédito aqui é o das agências bancárias localizadas em Santos, e não crédito ao Porto ou ao comércio exterior; o Comex Stat cobre o comércio exterior marítimo, não toda a movimentação do porto.

O texto escrito (versões do artigo) está em [`docs/artigo/`](docs/artigo/).

## Como reproduzir

```bash
cd src
python merge_datasets.py
```

Gera `painel_2015_2026.csv` e `painel_2015_2025.csv` em `data/processed/` a partir dos arquivos brutos em `data/raw/`. Depois:

```bash
python build_modeling_panel.py
```

Gera `painel_modelagem_2015_2025.csv` (o painel com o crédito sem o Bradesco), lido pelos notebooks 11 e 12.

Para rodar os notebooks, instale antes as dependências:

```bash
pip install -r requirements.txt
```

Observação: os notebooks 01 a 09 leem os dados direto das URLs raw deste repositório no GitHub, então precisam de conexão com a internet. Os notebooks 10 a 12 leem da pasta local `data/` quando ela existe e usam as URLs do GitHub caso contrário.

## Licença

Code is licensed under MIT (see LICENSE). Written analysis and report content are licensed under CC BY 4.0.

Os dados brutos em `data/raw/` continuam sujeitos aos termos de dados abertos das respectivas fontes originais (BCB, MDIC) — a licença deste repositório cobre o código e a análise produzidos pelo grupo, não os dados de origem.
