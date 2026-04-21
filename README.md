# FinancialSense
Pipeline ETL em Python com dados do Banco Central (SGS) para análise de indicadores macroeconômicos brasileiros — IPCA, Selic, Endividamento e Comprometimento de Renda. Visualizado em Power BI.

---

## 📊 Dashboard

<img width="818" height="433" alt="image" src="https://github.com/user-attachments/assets/854eab50-e0d4-4367-87f5-a8bc54665987" />


https://drive.google.com/file/d/1pxgw43wTE5fE9g9FNU1bZ6NNMJHU2mcM/view?usp=drive_link


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
├── src/
│   ├── extractor.py       # Filtro 1: Extração via API do BACEN
│   └── transformer.py     # Filtro 2 e 3: Transformação e Consolidação
├── data/                  # Gerado localmente — ignorado pelo Git
├── main.py                # Orquestrador do pipeline
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

Leia a análise completa no LinkedIn: [Juros ou Inflação: O que realmente está sufocando a renda das famílias?](#) ← substitua pelo link do post
