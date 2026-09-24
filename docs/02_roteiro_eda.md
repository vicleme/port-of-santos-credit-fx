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
| `03_agencias_ativo_credito.ipynb` | Extensão pontual: verifica formalmente — correlação de verdade, evolução ano a ano — se o fechamento de agências bancárias físicas em Santos (ESTBAN) explica o padrão de `ativo_total`/`credito_total` observado no passo 1. Testado por banco desde o início (não só como patch para um ano suspeito), o que permitiu checar mês ausente por instituição na série inteira 2015-2025: buraco de reporte só aparece em 2025 (Itaú, Santander, BB) — nenhum ano anterior, incluindo os de maior oscilação (2016, 2020, 2022, 2023), tem esse problema. Isso descarta, ao menos nesta fonte, a hipótese de que os saltos grandes da série sejam artefato de qualidade de dado disfarçado de volatilidade real, e fortalece a conclusão de "causa em aberto" em vez de deixar parecer efeito de dado sujo. Conclusão: não há uma quebra pontual em 2019-2020 (hipótese inicial) — a série é estruturalmente volátil o tempo todo, e o fechamento de agências (padrão suave e monotônico) explica só uma fração pequena da tendência de queda, não a volatilidade. Causa da volatilidade fica em aberto para os passos de Correlação (4) e Estacionariedade/Decomposição (5-6). A série de agências em 2025 tem limitação de qualidade de dado (meses ausentes por banco) ainda não tratada; a série é confiável de 2015 a 2024. |
| `04_temporal_painel_2015_2025.ipynb` | Passo 2 (temporal). |
| `05_tratamento_nans.ipynb` | Passo 3 (tratamento dos NaNs). |
| `06_correlacao.ipynb` | Passo 4 (correlação, sobre os níveis das séries). |
| `07_estacionariedade.ipynb` | Passo 5 (estacionariedade, teste ADF). |
| `08_decomposicao.ipynb` | Passo 6 (decomposição em tendência, sazonalidade e resíduo). |
| `09_correlacao_diferenciada.ipynb` | Extensão pontual do passo 4: refaz a correlação em primeira diferença, a partir do resultado do passo 5 (as séries com tendência precisam de Δ para evitar correlação espúria). |

**Convenção de numeração:** o número do notebook segue a **ordem de criação**, não o número do passo; a correspondência entre notebook e passo é a da tabela acima. Os notebooks `02`, `03` e `09` são extensões pontuais que nasceram de perguntas levantadas por um passo (`02` e `03` pela univariada, `09` pela estacionariedade) e por isso não correspondem a um passo próprio.

---

## Perguntas em aberto para a fase de contexto

A EDA quantitativa mostra **o que** aconteceu nas séries, mas não **por quê**. As perguntas abaixo surgiram durante os notebooks e ficam registradas para a fase de pesquisa de contexto (notícias, relatórios, decisões de política monetária), que será planejada em roteiro próprio, com critérios metodológicos de seleção e cruzamento de fontes, depois de encerrada a EDA.

| # | Pergunta | Origem | Observação |
|---|---|---|---|
| 1 | Por que o câmbio disparou em 2020? | `04_temporal_painel_2015_2025.ipynb` | A alta de 2020 (+35%) é um dos dois choques da série, junto com 2015/16. A estatística sozinha não responde ao "por quê": isso exige contexto externo. |
| 2 | O degrau de `credito_total` em **agosto/2019** (de 30,3 para 6,5 bilhões, -79% em um único mês) é mudança real de crédito em Santos ou artefato de reporte/reclassificação no ESTBAN? | `07_estacionariedade.ipynb`, seção 5 | A descrição "queda em 2020" no `04` vem de comparação entre médias anuais. Na visão mensal, o degrau precede 2020. Para separar as hipóteses seria preciso baixar o ESTBAN por banco em 2019 (como foi feito para 2025 no `03`). |

**Decisão metodológica que depende da pergunta 2:** como `credito_total` entra nos passos seguintes (em nível, em primeira diferença, ou em nível com variável indicadora para o período pós-degrau). O ADF sozinho não resolve, porque a série tem quebra dominante (ver `07`, seções 5 e 6).

Novas perguntas levantadas pelos passos 6 em diante devem ser acrescentadas a esta tabela.