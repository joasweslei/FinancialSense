from src import extractor
from src import transformer
from datetime import date

# Série 433 - Histórico do IPCA, mede inflação
# Série 1178 - Selic, taxa básica de juros mensal
# Série 21082 - Endividamento das famílias 
# Série 21084 - Comprometimento de renda das famílias 

start_date = date(2016, 5, 1)

df_ipca = extractor.fetch_sgs_data(433)
df_selic = extractor.fetch_sgs_data_by_date(1178, start_date)
df_dolar = extractor.fetch_sgs_data_by_date(3695, start_date)
df_endividamento = extractor.fetch_sgs_data(21082)
df_comprometimento_renda = extractor.fetch_sgs_data(21084)

df_ipca = transformer.transform_ipca(df_ipca, "IPCA")
df_selic = transformer.transform_data(df_selic, "Selic Efetiva (%) a.a.")
df_dolar = transformer.transform_data(df_dolar, "Dolar Mensal")
df_endividamento = transformer.transform_data(df_endividamento, "Endividamento das famílias")
df_comprometimento_renda  = transformer.transform_data(df_comprometimento_renda, "Comprometimento de renda das famílias")

df_indicadores_macroeconomicos = transformer.consolidar_indicadores_macroeconomicos(
    df_ipca, df_selic, df_dolar, df_endividamento, df_comprometimento_renda )

df_indicadores_macroeconomicos.to_parquet("./data/indicadores_macroeconomicos.parquet")


'''

df_eventos_economicos = extractor.get_economic_events()
df_eventos_economicos.to_parquet("./data/eventos_economicos.parquet")
'''