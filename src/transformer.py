import pandas as pd
from datetime import date

"""
    Filtro 2: Limpeza e Tipagem
"""
def transform_data(df, col_name):
    # 1. Conversão de Tipos
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce') # 'coerce' transforma erros em NaN
    
    # 2. Verificação de NaN
    nulos = df['valor'].isna().sum()
    if nulos > 0:
        print(f"Atenção: A coluna {col_name} possui {nulos} valores nulos.")
        # Opcional: df = df.dropna(subset=['valor']) ou preencher com o valor anterior
        # df['valor'] = df['valor'].ffill() 
    
    # 3. Renomeação e Finalização
    df.rename(columns={'valor': col_name}, inplace=True)
    df = add_relative_measures(df, col_name)
    
    print(f"--- Estatísticas de {col_name} ---")
    return df

def transform_ipca(df, col_name):
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df = df.sort_values('data')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)
    
    # Filtre para o período que você vai usar no Sicoob (ex: a partir de 2016)
    # antes de começar a multiplicar os valores.
    df = df[df['data'] >= '2016-05-01'].copy()
    
    # Agora o cumprod() só vai multiplicar valores pequenos (0.5%, 1%, etc.)
    df[col_name + '_Index'] = (1 + (df['valor'] / 100)).cumprod() * 100
    
    # Normaliza para que o primeiro valor do recorte seja 100
    df[col_name + '_Index'] = (df[col_name + '_Index'] / df[col_name + '_Index'].iloc[0]) * 100
    
    df.rename(columns={'valor': col_name}, inplace=True)
    return df

def add_relative_measures(df, col_name):
    # Variação percentual mês a mês (MoM)
    df[col_name + '_var_mensal'] = df[col_name].pct_change()
    
    # Índice Base 100 (Normalização pelo primeiro valor da série)
    df[col_name + '_Index'] = (df[col_name] / df[col_name].iloc[0]) * 100
    
    return df

def create_date_dimension(start_date, end_date):
    """Filtro Auxiliar: Gera uma Dimensão Tempo completa."""
    df_date = pd.DataFrame({'data': pd.date_range(start=start_date, end=end_date, freq='MS')})
    df_date['ano'] = df_date['data'].dt.year
    df_date['mes'] = df_date['data'].dt.month
    df_date['trimestre'] = df_date['data'].dt.quarter
    df_date['nome_mes'] = df_date['data'].dt.month_name()
    return df_date

# Unificando os dados (Duto de Integração)
def consolidar_indicadores_macroeconomicos(df_ipca, df_selic, df_dolar, df_endividamento, df_comprometimento_renda):
    df_calendario = create_date_dimension( date(1980, 1, 1), date.today() )
    
    df_final = df_calendario.merge(df_ipca, on='data', how='left') \
                            .merge(df_selic, on='data', how='left') \
                            .merge(df_dolar, on='data', how='left') \
                            .merge(df_endividamento, on='data', how='left') \
                            .merge(df_comprometimento_renda, on='data', how='left')

    # Filtrar apenas o período onde temos dados de endividamento (2011 em diante)
    condicao_data = df_final['data'] >= '2011-03-01'
    df_final = df_final[ condicao_data ]

    return df_final