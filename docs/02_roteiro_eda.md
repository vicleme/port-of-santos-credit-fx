# Roteiro da EDA — `01_eda_painel_2015_2025`

Este documento registra a sequência de passos planejada para a análise exploratória (EDA) do painel mensal (`painel_2015_2025.csv`), e como os notebooks do projeto se encaixam nela.

---

## Os 6 passos

| # | Passo | O que faz |
|---|---|---|
| 1 | **Univariada** | Histograma/boxplot de cada série (câmbio, crédito, exportação/importação FOB e kg) pra entender a distribuição de cada variável isoladamente e localizar outliers. |
| 2 | **Temporal** | Plotar cada série ao longo do tempo (2015–2025). Como é painel mensal, isso já mostra visualmente coisas como a disparada do câmbio em 2015/16 e 2020, sazonalidade em exportação/importação, e se o crédito acompanha ou não o câmbio. |
| 3 | **Tratamento dos NaNs** | Decidir e documentar: dropar os meses sem dado, interpolar, ou deixar como está e tratar caso a caso na modelagem. |
| 4 | **Correlação** | Matriz de correlação entre câmbio, `credito_total`, `exportação_fob`, `importação_fob`. Primeiro indício (não prova) da relação que o objetivo geral do projeto busca. |
| 5 | **Estacionariedade** | Teste de Dickey-Fuller (ADF) em cada série — obrigatório antes de qualquer regressão ou causalidade de Granger. O risco de regressão espúria é alto com séries que têm tendência, e praticamente todas as séries do painel têm. |
| 6 | **Decomposição** | Tendência/sazonalidade/resíduo de pelo menos câmbio e `exportação_fob`, pra visualizar se dá pra separar efeito cambial de efeito sazonal do comércio. |

---

## Como os notebooks se encaixam

| Notebook | Relação com o roteiro |
|---|---|
| `01_eda_painel_2015_2025.ipynb` | Passo 1 (univariada). |
| `02_outlier_importacao_2021.ipynb` | Extensão pontual: detalha por NCM (Comex Stat) o outlier de `importação_kg` encontrado no passo 1 (set–out/2021). |
| `03_agencias_ativo_credito.ipynb` | Extensão pontual: verifica formalmente — correlação de verdade, evolução ano a ano — se o fechamento de agências bancárias físicas em Santos (ESTBAN) explica o padrão de `ativo_total`/`credito_total` observado no passo 1. Conclusão: não há uma quebra pontual em 2019-2020 (hipótese inicial) — a série é estruturalmente volátil o tempo todo, e o fechamento de agências (padrão suave e monotônico) explica só uma fração pequena da tendência de queda, não a volatilidade. Causa da volatilidade fica em aberto. Registra também uma limitação de qualidade de dado na série de agências em 2025. |
| `04_...` em diante | Retomam a sequência do roteiro em ordem: temporal → NaNs → correlação → estacionariedade → decomposição. |

**Convenção de numeração:** os notebooks `02` e `03` nasceram de perguntas levantadas pela univariada (passo 1) e não seguem a ordem numérica do roteiro — são extensões pontuais do `01`. A partir do `04`, a numeração volta a acompanhar a sequência dos passos listados acima.
