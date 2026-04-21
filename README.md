# FinancialSense
Pipeline ETL em Python com dados do Banco Central (SGS) para análise de indicadores macroeconômicos brasileiros — IPCA, Selic, Endividamento e Comprometimento de Renda. Inclui modelo de Regressão Linear Múltipla para mensurar o impacto das liberações do FGTS no endividamento das famílias. Visualizado em Power BI.

---

## 📊 Dashboard

<img width="1544" height="817" alt="image" src="https://github.com/user-attachments/assets/558b6d36-fc24-454a-9b3c-fc1af501ce9a" />


Acesse aqui ao dashboard: https://drive.google.com/file/d/1pxgw43wTE5fE9g9FNU1bZ6NNMJHU2mcM/view?usp=drive_link


## 💡 Insight Principal

A análise revelou que a **inflação acumulada (IPCA) tem correlação de 0,48** com o comprometimento de renda das famílias, enquanto a **Selic apresenta correlação de apenas 0,13** — sugerindo que a pressão inflacionária crônica é o principal driver do endividamento familiar, não o custo do crédito.

---

## 🏗️ Arquitetura: Duto e Filtro

O projeto segue o padrão **Pipe and Filter**, onde cada etapa é independente e responsável por uma única transformação:

```
API Banco Central (SGS)
        │
        ▼
┌─────────────────┐
│  Filtro 1       │  extractor.py
│  Extração       │  → Coleta as séries temporais via REST
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Filtro 2       │  transformer.py
│  Transformação  │  → Normalização Base 100, encadeamento IPCA, tipagem
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Filtro 3       │  transformer.py → consolidar_indicadores_macroeconomicos()
│  Consolidação   │  → Merge das séries em um único arquivo Parquet
└────────┬────────┘
         │
         ▼
  indicadores_macroeconomicos.parquet
         │
         ▼
     Power BI
```

---

## 📈 Séries Utilizadas

| Série SGS | Indicador | Descrição |
|-----------|-----------|-----------|
| 433 | IPCA | Índice de inflação ao consumidor |
| 1178 | Selic Efetiva | Taxa básica de juros (% a.a.) |
| 3695 | Dólar | Cotação mensal |
| 21082 | Endividamento | Endividamento das famílias (%) |
| 21084 | Comprometimento de Renda | % da renda comprometida com dívidas |

Fonte: [API SGS — Banco Central do Brasil](https://www.bcb.gov.br/estabilidadefinanceira/creditosfpj)

---

## 🤖 Modelo de Machine Learning

Regressão Linear Múltipla para mensurar o efeito causal de cada liberação 
do FGTS sobre o endividamento, controlando por Selic e IPCA.

**R² = 0.61** — o modelo explica 61% da variação no endividamento.

| Evento | Coeficiente | Efeito |
|---|---|---|
| Início Saques FGTS Inativo (2017) | +0.478 | ↑ Aumentou endividamento |
| Auxílio Emergencial / Pandemia (2020) | +0.393 | ↑ Aumentou endividamento |
| Saque Extraordinário FGTS (2022) | -0.410 | ↓ Reduziu endividamento |

> Os saques de 2017 e 2020 incentivaram novas dívidas. O saque de 2022 
> foi usado para quitar dívidas existentes num contexto de juros altos.


## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/joasweslei/FinancialSense.git
cd FinancialSense

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Crie a pasta de saída
mkdir data

# Execute o pipeline
python main.py
```

O arquivo `data/indicadores_macroeconomicos.parquet` será gerado e pode ser importado diretamente no Power BI.

---

## 📁 Estrutura do Projeto

```
FinancialSense/
├── notebooks/
│   └── analise_impacto_fgts.ipynb  # Análise completa com gráficos
├── src/
│   ├── extractor.py
│   ├── transformer.py
│   └── regressao_multipla.py
├── data/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![Parquet](https://img.shields.io/badge/Formato-Parquet-brightgreen)

---

## 📝 Artigo

Leia a análise completa no LinkedIn: https://www.linkedin.com/posts/joas-baia_juros-ou-infla%C3%A7%C3%A3o-o-que-realmente-est%C3%A1-sufocando-activity-7452155689709436928-erzy?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAAqdHX4BKoWnoyyfYHVPZ0HMjDAxAyIUzHE
