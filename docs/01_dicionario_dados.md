# Dicionário de dados — `painel_2015_2025.csv`

Este documento explica o que cada coluna do painel representa, de onde vem e como interpretar seus valores. Painel mensal, uma linha por (ano, mês), 2015–2025.

---

## Identificação

| Coluna | O que é |
|---|---|
| `ano` | Ano de referência do mês (2015–2025). |
| `mes` | Mês de referência (1 a 12). |

---

## Câmbio

| Coluna | Fonte | O que significa em linguagem simples |
|---|---|---|
| `cambio_venda` | BCB SGS, série 3696 | Quantos reais custava 1 dólar americano, na taxa de **venda**, no último dia útil do mês (PTAX). É a referência que bancos e empresas usam para converter valores entre real e dólar. Quando esse número sobe, o real está "mais fraco" (desvalorizado) frente ao dólar — importar fica mais caro, exportar fica mais vantajoso em reais. |

---

## Crédito bancário (fonte: BCB ESTBAN, município de Santos)

O ESTBAN é o balanço mensal que cada agência bancária no Brasil é obrigada a enviar ao Banco Central. Os valores abaixo são a soma de todas as agências bancárias localizadas no município de Santos.

| Coluna | Verbete ESTBAN | O que significa em linguagem simples |
|---|---|---|
| `credito_total` | 160 | O total de todo o crédito (empréstimos e operações relacionadas) que os bancos com agência em Santos tinham concedido, somado, naquele mês. **Importante:** não é a soma das três colunas abaixo — é um agregado maior e independente, que inclui outras operações de crédito não detalhadas separadamente no painel. |
| `credito_emprestimos_titulos` | 161 | Uma parte específica do crédito total: empréstimos convencionais e títulos descontados (ex.: quando uma empresa antecipa o recebimento de uma duplicata/nota promissória junto ao banco). |
| `credito_financiamentos` | 162 | Outra parte do crédito total: financiamentos — operações de crédito atreladas a uma finalidade específica (ex.: financiar a compra de um equipamento, capital de giro vinculado). |
| `credito_outras_operacoes` | 171 | Demais operações de crédito que não se enquadram nas duas categorias acima (ex.: outras linhas específicas do balancete bancário). |

> Para a análise do PI2, o mais relevante costuma ser `credito_total` como indicador geral do volume de crédito bancário na praça de Santos — as três colunas de detalhamento ajudam a entender a composição, mas não somam ao total.

---

## Balanço bancário agregado (fonte: BCB ESTBAN, município de Santos)

| Coluna | Verbete ESTBAN | O que significa em linguagem simples |
|---|---|---|
| `ativo_total` | 399 | Tudo que os bancos com agência em Santos **possuem**, somado: dinheiro em caixa, aplicações, e principalmente os próprios empréstimos que fizeram (um empréstimo concedido é um "direito a receber" para o banco, então conta como um bem/ativo dele). |
| `passivo_total` | 899 | Tudo que esses bancos **devem**, somado — majoritariamente os depósitos de clientes (conta corrente, poupança, aplicações): o dinheiro que você guarda no banco é, contabilmente, uma dívida do banco com você. |

**Nota da EDA:** `ativo_total` e `passivo_total` são praticamente idênticos em quase todo o painel (120 dos 132 meses, com pequenas divergências de arredondamento nos outros 12). Isso acontece porque é a identidade contábil básica do balanço patrimonial: tudo que o banco possui (ativo) foi financiado por alguma fonte (passivo) — cada real emprestado veio de algum depósito ou captação. Na prática, as duas colunas carregam quase a mesma informação (o "tamanho" do sistema bancário em Santos), então é provável que só uma delas seja necessária na modelagem mais adiante.

---

## Comércio exterior (fonte: Comex Stat/MDIC, Porto de Santos, via marítima)

| Coluna | O que significa em linguagem simples |
|---|---|
| `exportação_fob` | Valor total (em dólares americanos, US$) de tudo que saiu do Brasil pelo Porto de Santos naquele mês, na modalidade **FOB** (*Free On Board*) — ou seja, o valor da mercadoria até ela ser colocada a bordo do navio, sem contar frete e seguro do trajeto internacional. É o valor "de venda" da carga exportada. |
| `importação_fob` | Mesma lógica, mas para o que **entrou** no Brasil pelo Porto de Santos: valor em US$ das mercadorias importadas, na modalidade FOB (valor da mercadoria no porto de origem, sem frete/seguro internacional). |
| `exportação_kg` | Peso total, em quilogramas líquidos, de toda a carga exportada pelo Porto de Santos naquele mês. Mede o **volume físico** movimentado, complementando o valor em dólares. |
| `importação_kg` | Peso total, em quilogramas líquidos, de toda a carga importada pelo Porto de Santos naquele mês. |

> Por que ter valor (US$) *e* peso (kg) juntos: eles respondem perguntas diferentes. Valor em US$ mede o tamanho econômico do comércio; peso em kg mede o volume logístico/físico movimentado no porto — os dois podem se mover de formas diferentes (ex.: exportar menos toneladas de um produto caro pode gerar mais dólares do que exportar muitas toneladas de um produto barato).

---

## Painel de modelagem — `painel_modelagem_2015_2025.csv`

Arquivo derivado, gerado por `src/build_modeling_panel.py` (saída em `data/processed/`). Tem as mesmas colunas do painel principal (mesmas fontes e significados acima) mais uma coluna nova, `credito_ex_bradesco`, posicionada logo depois de `credito_total`. As colunas `credito_emprestimos_titulos`, `credito_financiamentos`, `credito_outras_operacoes`, `ativo_total` e `passivo_total` não entram neste arquivo.

| Coluna | Fonte | O que significa em linguagem simples |
|---|---|---|
| `credito_ex_bradesco` | ESTBAN por banco (`data/raw/estban_verbetes_santos_2015-2025_por_banco.csv`), verbete 160 | O mesmo crédito total (verbete 160) das agências de Santos, **somando todos os bancos exceto o Bradesco** (CNPJ básico 60746948). Existe porque o degrau de agosto/2019 em `credito_total` vem quase todo de uma única instituição, o Bradesco; sem ele, a série deixa de ter esse salto. A decisão e a comparação com as alternativas estão no notebook `10_estban_por_banco_degrau_2019`. |

**Cobertura:** a coluna só está preenchida de 2015-01 a 2024-12 (120 meses); os 12 meses de 2025 ficam vazios (NaN). Em 2025 há buracos de reporte de bancos específicos (Itaú, Santander e Banco do Brasil), e somar só os bancos que sobram criaria quedas artificiais no agregado.

**Como interpretar:** em valores correntes, em reais, como `credito_total`. A participação dos demais bancos no total varia muito ao longo do tempo (de cerca de 19% a 99%), por isso `credito_ex_bradesco` não é uma fração constante de `credito_total`. Para a modelagem (notebooks 11 e 12), é a série de crédito usada no lugar de `credito_total`.

---

## Fontes

- Câmbio: BCB SGS, série 3696 — `https://api.bcb.gov.br/dados/serie/bcdata.sgs.3696/dados`
- Crédito e balanço bancário: BCB ESTBAN, via Base dos Dados (`basedosdados.br_bcb_estban.municipio`), município de Santos (IBGE 3548500)
- Crédito por banco (usado em `credito_ex_bradesco`): BCB ESTBAN por instituição e verbete, mesmo recorte de Santos, em `data/raw/estban_verbetes_santos_2015-2025_por_banco.csv`
- Comércio exterior: Comex Stat — MDIC, módulo "Geral", filtro Via=Marítima + URF=0817800 (Porto de Santos)
